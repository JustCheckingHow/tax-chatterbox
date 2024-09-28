import json

from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger

from . import chat_utils


class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    def parse_messages_history(self, messages):
        messages_parsed = []
        for msg in messages:
            if msg["sender"] == "user":
                messages_parsed.append({"role": "user", "content": msg["message"]})
            elif msg["sender"] == "ai":
                messages_parsed.append({"role": "assistant", "content": msg["message"]})
        return messages_parsed

    async def send_on_the_fly(self, method, message, history, command, final_command, required_info=None):
        if required_info is None:
            res = await method(
                message,
                history,
                callback=lambda x: self.send(
                    text_data=json.dumps({"message": x, "command": command, "history": history})
                ),
            )
        else:
            res = await method(
                message,
                history,
                required_info,
                callback=lambda x: self.send(
                    text_data=json.dumps({"message": x, "command": command, "history": history})
                ),
            )
        await self.send(text_data=json.dumps({"message": res, "command": final_command, "history": history}))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.info(f"Received message: {text_data_json}")

        message = text_data_json["text"]
        required_info = text_data_json["required_info"]
        messages = text_data_json["history"]
        is_necessary = text_data_json["is_necessary"]
        messages_parsed = self.parse_messages_history(messages)

        intent = await chat_utils.recognize_question(message, messages_parsed)
        logger.info(f"Intent: {intent}")
        if intent == "inne":
            await self.send_on_the_fly(
                chat_utils.refuse_to_answer, message, messages_parsed, "basicFlowPartial", "basicFlowComplete"
            )
            return
        elif intent == "pytanie":
            await self.send_on_the_fly(
                chat_utils.scrap_ddgo_for_info, message, messages_parsed, "basicFlowPartial", "basicFlowComplete"
            )
            return

        # Extract information from user message and prompt them for missing info
        answer = await chat_utils.parse_info(message, messages_parsed, required_info)
        # Remove unchanged values
        answer = {k: v for k, v in answer.items() if str(v).strip() != str(required_info[k]).strip()}
        required_info.update(answer)
        await self.send(text_data=json.dumps({"message": answer, "command": "informationParsed"}))

        # Check whether the form is even necessary
        answer = await chat_utils.verify_if_necessary(message, messages_parsed)
        if is_necessary == "unknown" or answer == "nie wiem":
            logger.info(f"AI response: {answer}")
            await self.send(text_data=json.dumps({"message": answer, "command": "isNecessary"}))

            await self.send_on_the_fly(
                chat_utils.question_if_necessary, message, messages_parsed, "basicFlowPartial", "basicFlowComplete"
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
            )
            return

        # Check what tax rate should be applied in the case
        if "stawka_podatku" not in required_info:
            tax_rate_ans = await chat_utils.compute_tax_rate(message, messages_parsed)
            required_info.update({"tax_rate": tax_rate_ans["stawka"]})
            await self.send(text_data=json.dumps({"message": tax_rate_ans["argument"], "command": "basicFlowComplete"}))
        # # Send message to AI consumer
        # Send message to AI consumer
        await self.send_on_the_fly(
            chat_utils.get_ai_response,
            message,
            messages_parsed,
            "basicFlowPartial",
            "basicFlowComplete",
            required_info=required_info,
        )
