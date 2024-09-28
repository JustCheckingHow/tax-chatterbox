import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import openai

# Assuming you have set up your OpenAI API key in your environment variables
openai.api_key = "your-openai-api-key"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "tax_chat"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': 'user'
            }
        )

        # Send message to AI consumer
        await self.channel_layer.send(
            'ai_response',
            {
                'type': 'ai_message',
                'message': message,
                'response_channel': self.channel_name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def ai_message(self, event):
        message = event['message']
        response_channel = event['response_channel']

        # Get AI response
        ai_response = await self.get_ai_response(message)

        # Send AI response back to the chat consumer
        await self.channel_layer.send(
            response_channel,
            {
                'type': 'chat_message',
                'message': ai_response,
                'sender': 'ai'
            }
        )

    @sync_to_async
    def get_ai_response(self, message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful tax assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"An error occurred: {str(e)}"