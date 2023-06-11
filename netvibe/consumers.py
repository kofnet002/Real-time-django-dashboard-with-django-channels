import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Statistic, DataItem


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # To get the dynamic url name
        dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f'netvibe-{dashboard_slug}'  # create group name

       # Add websocket connection to group name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"connection closed with code: {close_code}")

        # Remove websocket connection from group name
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]

        dashboard_slug = self.dashboard_slug
        # call save function to save data to db
        await self.save_data_item(sender, message, dashboard_slug)

        # Send messages to all members in the group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'statistics_message',  # method for sending message
            'message': message,
            'sender': sender
        })

    # Method for sending message
    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def create_data_item(self, sender, message, slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(
            statistic=obj,
            value=message,
            owner=sender
        )

    async def save_data_item(self, sender, message, slug):
        await self.create_data_item(sender, message, slug)
