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

    async def send_on_the_fly(self, method, message, history, command, final_command):
        res = await method(
            message,
            history,
            callback=lambda x: self.send(text_data=json.dumps({"message": x, "command": command, "history": history})),
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
        if intent == "inne":
            await self.send_on_the_fly(
                chat_utils.refuse_to_answer, message, messages_parsed, "basicFlowPartial", "basicFlowComplete"
            )
            return

        # Extract information from user message and prompt them for missing info
        answer = await chat_utils.parse_info(message, messages_parsed, required_info)
        logger.info(f"AI response: {answer}")
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

        # Send message to AI consumer
        await self.send_on_the_fly(
            chat_utils.get_ai_response, message, messages_parsed, "basicFlowPartial", "basicFlowComplete"
        )
