from channels.generic.websocket import AsyncWebsocketConsumer
from room.models import Room
from room.game import connectedPlayerCount, step, message1, message2, \
    message3, message4
from asgiref.sync import async_to_sync
import json
import threading
from apscheduler.schedulers.background import BackgroundScheduler


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        room = Room.objects.get(name=self.room_name)
        max_num = room.max_num
        cur_num = room.cur_num
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        if max_num == 2:
            if cur_num == 0:
                room.cur_num = 1
                room.player1 = self.player_name
            elif cur_num == 1:
                room.cur_num = 2
                room.player2 = self.player_name
            else:
                await self.close()
            room.save()
        elif max_num == 4:
            if cur_num == 0:
                room.cur_num = 1
                room.player1 = self.player_name
            elif cur_num == 1:
                room.cur_num = 2
                room.player2 = self.player_name
            elif cur_num == 2:
                room.cur_num = 3
                room.player3 = self.player_name
            elif cur_num == 3:
                room.cur_num = 4
                room.player4 = self.player_name
            else:
                await self.close()
            room.save()
        else:
            await self.close()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'type': 'join_room',
                    'message': self.player_name
                })
            }
        )
        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        room = Room.objects.get(name=self.room_name)
        max_num = room.max_num
        cur_num = room.cur_num
        player1 = room.player1
        player2 = room.player2
        player3 = room.player3
        player4 = room.player4
        if max_num == 2:
            if cur_num == 1:
                room.delete()
            elif cur_num == 2:
                if self.player_name == player1:
                    room.player1 = player2
                    room.player2 = ''
                    room.ready2 = 0
                    room.cur_num = 1
                    room.save()
                elif self.player_name == player2:
                    room.player2 = ''
                    room.ready2 = 0
                    room.cur_num = 1
                    room.save()
        elif max_num == 4:
            if cur_num == 1:
                room.delete()
            elif cur_num == 2:
                if self.player_name == player1:
                    room.player1 = player2
                    room.player2 = ''
                    room.ready2 = 0
                    room.cur_num = 1
                    room.save()
                elif self.player_name == player2:
                    room.player2 = ''
                    room.ready2 = 0
                    room.cur_num = 1
                    room.save()
            elif cur_num == 3:
                if self.player_name == player1:
                    room.player1 = player2
                    room.player2 = player3
                    room.player3 = ''
                    room.ready2 = room.ready3
                    room.ready3 = 0
                    room.cur_num = 2
                    room.save()
                elif self.player_name == player2:
                    room.player2 = player3
                    room.player3 = ''
                    room.ready2 = room.ready3
                    room.ready3 = 0
                    room.cur_num = 2
                    room.save()
                elif self.player_name == player3:
                    room.player3 = ''
                    room.ready3 = 0
                    room.cur_num = 2
                    room.save()
            elif cur_num == 4:
                if self.player_name == player1:
                    room.player1 = player2
                    room.player2 = player3
                    room.player3 = player4
                    room.player4 = ''
                    room.ready2 = room.ready3
                    room.ready3 = room.ready4
                    room.ready4 = 0
                    room.cur_num = 3
                    room.save()
                elif self.player_name == player2:
                    room.player2 = player3
                    room.player3 = player4
                    room.player4 = ''
                    room.ready2 = room.ready3
                    room.ready3 = room.ready4
                    room.ready4 = 0
                    room.cur_num = 3
                    room.save()
                elif self.player_name == player3:
                    room.player3 = player4
                    room.player4 = ''
                    room.ready3 = room.ready4
                    room.ready4 = 0
                    room.cur_num = 3
                    room.save()
                elif self.player_name == player4:
                    room.player4 = ''
                    room.ready4 = 0
                    room.cur_num = 3
                    room.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'type': 'leave_room',
                    'message': self.player_name
                })
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        room = Room.objects.get(name=self.room_name)
        if type == 'change_map':
            room.game_map = message
            room.save()
        elif type == 'get_ready':
            name = message
            if name == room.player2:
                room.ready2 = 1
            elif name == room.player3:
                room.ready3 = 1
            elif name == room.player4:
                room.ready4 = 1
            room.save()
        elif type == 'cancel_ready':
            name = message
            if name == room.player2:
                room.ready2 = 0
            elif name == room.player3:
                room.ready3 = 0
            elif name == room.player4:
                room.ready4 = 0
            room.save()
        elif type == 'set_password':
            password = message
            room.hasPassword = 1
            room.password = password
            room.save()
        elif type == 'cancel_password':
            room.hasPassword = 0
            room.save()
        elif type == 'change_password':
            password = message
            room.password = password
            room.save()
        elif type == 'ready':
            if room.readyNum + 1 == room.max_num:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': json.dumps({
                            'type': 'start'
                        })
                    }
                )
            room.readyNum += 1
            room.save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(message)


class GameComsumer(AsyncWebsocketConsumer):

    def sendStep(self):
        try:
            m1 = message1[self.room_name]
        except Exception:
            m1 = ''
        try:
            m2 = message2[self.room_name]
        except Exception:
            m2 = ''
        try:
            m3 = message3[self.room_name]
        except Exception:
            m3 = ''
        try:
            m4 = message4[self.room_name]
        except Exception:
            m4 = ''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'frameID': step[self.room_name],
                    "playerData": [
                        [m1],
                        [m2],
                        [m3],
                        [m4]
                    ],
                })
            })
        message1[self.room_name] = ''
        message2[self.room_name] = ''
        message3[self.room_name] = ''
        message4[self.room_name] = ''
        step[self.room_name] += 1

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        try:
            connectedPlayerCount[self.room_name] += 1
        except Exception:
            connectedPlayerCount[self.room_name] = 1
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        room = Room.objects.get(name=self.room_name)
        if self.player_name == room.player1:
            self.message = message1
        elif self.player_name == room.player2:
            self.message = message2
        elif self.player_name == room.player3:
            self.message = message3
        elif self.player_name == room.player4:
            self.message = message4

        self.max_num = room.max_num
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        if connectedPlayerCount[self.room_name] == room.cur_num:
            step[self.room_name] = 0
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': json.dumps({
                        'step': 0,
                        'message': 'start'
                    })
                })
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.sendStep, 'interval', seconds=0.06)
            scheduler.start()
        await self.accept()

    async def disconnect(self, code):
        connectedPlayerCount[self.room_name] -= 1
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['action']
        self.message[self.room_name] = message

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(message)
