import json

from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger

from . import chat_utils


class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.info(f"Received message: {text_data_json}")

        message = text_data_json["text"]
        required_info = text_data_json["required_info"]
        messages = text_data_json["history"]
        is_necessary = text_data_json["is_necessary"]

        messages_parsed = []
        for msg in messages:
            if msg["sender"] == "user":
                messages_parsed.append({"role": "user", "content": msg["message"]})
            elif msg["sender"] == "ai":
                messages_parsed.append({"role": "assistant", "content": msg["message"]})

        # Check whether the form is even necessary
        if is_necessary == "unknown":
            answer = await chat_utils.verify_if_necessary(message, messages_parsed)
            logger.info(f"AI response: {answer}")
            await self.send(text_data=json.dumps({"message": answer, "command": "isNecessary"}))

            if is_necessary == "unknown":
                res = await chat_utils.question_if_necessary(
                    message,
                    messages_parsed,
                    lambda x: self.send(text_data=json.dumps({"message": x, "command": "basicFlowPartial"})),
                )
                await self.send(text_data=json.dumps({"message": res, "command": "basicFlowComplete"}))
                return

        # Extract information from user message and prompt them for missing info
        answer = await chat_utils.parse_info(message, required_info)
        logger.info(f"AI response: {answer}")
        await self.send(text_data=json.dumps({"message": answer, "command": "informationParsed"}))

        # Send message to AI consumer
        answer = await chat_utils.get_ai_response(
            message,
            messages_parsed,
            required_info=[i for i in required_info if required_info[i].strip() == ""],
            callback=lambda x: self.send(text_data=json.dumps({"message": x, "command": "basicFlowPartial"})),
        )
        logger.info(f"AI response: {answer}")
        await self.send(text_data=json.dumps({"message": answer, "command": "basicFlowComplete"}))
