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

        if required_info:
            answer = await chat_utils.parse_info(message, required_info)
            logger.info(f"AI response: {answer}")
            await self.send(
                text_data=json.dumps(
                    {"message": answer, "command": "informationParsed"}
                )
            )

        # Send message to AI consumer
        answer = await chat_utils.get_ai_response(
            message,
            callback=lambda x: self.send(
                text_data=json.dumps({"message": x, "command": "basicFlowPartial"})
            ),
        )
        logger.info(f"AI response: {answer}")
        await self.send(
            text_data=json.dumps({"message": answer, "command": "basicFlowComplete"})
        )
