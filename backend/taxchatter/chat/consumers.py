import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger

from . import chat_utils
from .models import Conversation, Intent, Message

LANG_MAP = {
    "pl": "polsku",
    "uk": "ukraińsku",
    "en": "angielsku",
}

UNNECESSARY_QUESTIONS = [
    "Powiat",
    "Wojewodztwo",
    "KodKraju",
    "KodPocztowy",
    "UrzadSkarbowy",
]


class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.multidevice_idx = self.scope["url_route"]["kwargs"]["multidevice_idx"]

        # add to group
        await self.channel_layer.group_add("multidevice", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # if conversation is empty, delete it
        pass

    def parse_messages_history(self, messages):
        messages_parsed = []
        for msg in messages:
            if msg["sender"] == "user":
                messages_parsed.append(
                    {"role": "user", "content": msg["message"].replace("\n", " ")}
                )
            elif msg["sender"] == "ai":
                messages_parsed.append(
                    {"role": "assistant", "content": msg["message"].replace("\n", " ")}
                )
        return messages_parsed

    async def send_on_the_fly(
        self,
        method,
        message,
        history,
        command,
        final_command,
        required_info=None,
        obtained_info=None,
        language_setting="pl",
    ):
        if required_info is None:
            res = await method(
                message,
                history,
                callback=lambda x: self.send(
                    text_data=json.dumps(
                        {"message": x, "command": command, "history": history}
                    )
                ),
                language_setting=language_setting,
            )
        else:
            res = await method(
                message,
                history,
                required_info,
                obtained_info,
                callback=lambda x: self.send(
                    text_data=json.dumps(
                        {"message": x, "command": command, "history": history}
                    )
                ),
                language_setting=language_setting,
            )
        await self.send(
            text_data=json.dumps(
                {"message": res, "command": final_command, "history": history}
            )
        )

    async def mobile_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        msg_type = text_data_json.get("type", None)
        if msg_type == "mobileMessage":
            # send to group
            await self.channel_layer.group_send(
                "multidevice",
                {
                    "type": "mobile_message",
                    "message": {
                        "message": text_data_json["message"],
                        "command": "mobileMessage",
                        "fileBase64": text_data_json["fileBase64"],
                    },
                },
            )
            return

        message = text_data_json["text"]
        required_info = text_data_json["required_info"]
        obtained_info = text_data_json["obtained_info"]
        messages = text_data_json["history"]
        is_necessary = text_data_json["is_necessary"]
        language = text_data_json["language"]
        conversation_key = text_data_json["conversation_key"]

        for element in required_info:
            if list(element.keys())[0] in UNNECESSARY_QUESTIONS:
                required_info.remove(element)

        if conversation_key is None:
            conversation = await database_sync_to_async(Conversation.objects.create)()
            await self.send(
                text_data=json.dumps(
                    {
                        "messageId": str(conversation.conversation_key),
                        "command": "connect",
                    }
                )
            )
        else:
            conversation = await database_sync_to_async(Conversation.objects.get)(
                conversation_key=conversation_key
            )

        message_obj = Message(
            conversation=conversation, content=message, is_user_message=True
        )
        await database_sync_to_async(message_obj.save)()
        messages_parsed = self.parse_messages_history(messages)

        intent = await chat_utils.recognize_question(
            message, messages_parsed, language_setting=LANG_MAP[language]
        )
        logger.info(f"Intent: {intent}")

        intent_obj = Intent(intent=intent, message=message_obj)
        await database_sync_to_async(intent_obj.save)()

        if intent == "inne":
            await self.send_on_the_fly(
                chat_utils.refuse_to_answer,
                message,
                messages_parsed,
                "basicFlowPartial",
                "basicFlowComplete",
                language_setting=LANG_MAP[language],
            )
            return
        elif intent == "pytanie":
            await self.send_on_the_fly(
                chat_utils.scrap_ddgo_for_info,
                message,
                messages_parsed,
                "basicFlowPartial",
                "basicFlowComplete",
                language_setting=LANG_MAP[language],
            )
            return

        # Extract information from user message and prompt them for missing info
        answer = await chat_utils.parse_info(
            message,
            messages_parsed,
            required_info,
            language_setting=LANG_MAP[language],
        )
        # Remove unchanged values
        answer = {
            k: v
            for k, v in answer.items()
            if str(v).strip() != str(obtained_info.get(k, None)).strip()
        }
        obtained_info.update(answer)
        await self.send(
            text_data=json.dumps({"message": answer, "command": "informationParsed"})
        )

        # Check whether the form is even necessary
        answer = await chat_utils.verify_if_necessary(
            message, messages_parsed, language_setting=LANG_MAP[language]
        )
        if is_necessary == "unknown" or answer == "nie wiem":
            logger.info(f"AI response: {answer}")
            await self.send(
                text_data=json.dumps({"message": answer, "command": "isNecessary"})
            )

            await self.send_on_the_fly(
                chat_utils.question_if_necessary,
                message,
                messages_parsed,
                "basicFlowPartial",
                "basicFlowComplete",
                language_setting=LANG_MAP[language],
            )
            return

        # If we know that the form is not necessary, tell user why
        if answer == "nie musi" or not is_necessary:
            await self.send_on_the_fly(
                chat_utils.rationale_why_not_necessary,
                message,
                messages_parsed,
                "basicFlowPartial",
                "basicFlowComplete",
                language_setting=LANG_MAP[language],
            )
            return

        # Check what tax rate should be applied in the case
        if "stawka_podatku" not in obtained_info:
            tax_rate_ans = await chat_utils.compute_tax_rate(
                message, messages_parsed, language_setting=LANG_MAP[language]
            )
            logger.info(f"Tax rate answer: {tax_rate_ans}")
            obtained_info.update({"StawkaPodatku": tax_rate_ans["stawka"]})
            await self.send(
                text_data=json.dumps(
                    {
                        "message": {"stawka_podatku": tax_rate_ans["stawka"]},
                        "command": "informationParsed",
                    }
                )
            )
        # Send message to AI consumer
        await self.send_on_the_fly(
            chat_utils.get_ai_response,
            message,
            messages_parsed,
            "basicFlowPartial",
            "basicFlowComplete",
            required_info=required_info,
            obtained_info=obtained_info,
            language_setting=LANG_MAP[language],
        )
