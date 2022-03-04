import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
# from asgiref.sync import sync_to_async

class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    # @sync_to_async
    # def create_chat(self, msg, sender):
    #     print("in------------")
    #     new_msg = Message.objects.create(author=sender, context=msg)
    #     new_msg.save()
    #     return new_msg
    
    # @sync_to_async
    # def create_chat(self, msg, sender):
    #     print("in------------")
    #     new_msg = Message.objects.create(author=sender, context=msg)
    #     new_msg.save()
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await database_sync_to_async(Message.objects.create)(author=username, context=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass
