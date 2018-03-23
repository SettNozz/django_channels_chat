import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            'status-updates',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            'status-updates',
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.send(
            "thumbnails-generate",
            {
                'type': 'do_stuff',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



class ThumbnailConsumer(AsyncConsumer):
    async def do_stuff(self, event):
        message = event['message']

        while True:
            await asyncio.sleep(1)

            await self.channel_layer.group_send(
                'status-updates',
                {
                    'type': 'chat_message',
                    'message': 'hello world from ThumbnailConsumer!'
                }
            )

