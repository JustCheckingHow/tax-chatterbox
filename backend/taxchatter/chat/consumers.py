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
        message = text_data_json["message"]
        logger.info(f"Received message: {message}")

        # Send message to AI consumer
        answer = await chat_utils.get_ai_response(
            message,
            callback=lambda x: self.send(text_data=json.dumps({"message": x, "command": "basicFlowPartial"})),
        )
        logger.info(f"AI response: {answer}")
        await self.send(text_data=json.dumps({"message": answer, "command": "basicFlowComplete"}))
