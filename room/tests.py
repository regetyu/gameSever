from django.test import TestCase, Client
from room.models import Room


class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(
            name='testRoom',
            cur_num=1,
            max_num=2,
            game_map=0,
            player1='testPlayer1',
            player2='',
            player3='',
            player4='',
            ready2=0,
            ready3=0,
            ready4=0,
            hasPassword=0,
            password='',
            readyNum=0
        )

    def test_get_all_player(self):
        client = Client()
        response = client.get('/room/getAllPlayer/')
        self.assertEqual(response.content, b'testPlayer1\n')

    def test_create_room(self):
        client = Client()
        response = client.get('/room/create/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/room/create/', {
            'roomName': 'testRoom',
            'max': 4,
            'hasPassword': 0,
            'password': ''
        })
        self.assertEqual(response.content, b'room already exists')
        response = client.post('/room/create/', {
            'roomName': 'testRoom2',
            'max': 4,
            'hasPassword': 0,
            'password': ''
        })
        self.assertEqual(response.content, b'create room success')

    def test_get_all_room(self):
        client = Client()
        response = client.get('/room/getAll/')
        self.assertEqual(response.content,
                         b'testRoom\n1\n2\n0\ntestPlayer1\n\n\n\n0\n\t')

    def test_get_single_room(self):
        client = Client()
        response = client.get('/room/getSingle/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/room/getSingle/', {
            'roomName': '404'
        })
        self.assertEqual(response.content, b'room does not exist')
        response = client.post('/room/getSingle/', {
            'roomName': 'testRoom'
        })
        self.assertEqual(response.content,
                         b'testRoom\n1\n2\n0\ntestPlayer1'
                         b'\n\n\n\n0\n0\n0\n0\n\t')

    def test_verify(self):
        Room.objects.create(
            name='testRoom2',
            cur_num=1,
            max_num=2,
            game_map=0,
            player1='testPlayer2',
            player2='',
            player3='',
            player4='',
            ready2=0,
            ready3=0,
            ready4=0,
            hasPassword=1,
            password='password',
            readyNum=0
        )
        Room.objects.create(
            name='testRoom3',
            cur_num=2,
            max_num=2,
            game_map=0,
            player1='testPlayer3',
            player2='testPlayer4',
            player3='',
            player4='',
            ready2=0,
            ready3=0,
            ready4=0,
            hasPassword=1,
            password='',
            readyNum=0
        )
        client = Client()
        response = client.get('/room/verify/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/room/verify/', {
            'roomName': '404',
            'password': ''
        })
        self.assertEqual(response.content, b'room does not exist')
        response = client.post('/room/verify/', {
            'roomName': 'testRoom2',
            'password': '123'
        })
        self.assertEqual(response.content, b'password incorrect')
        response = client.post('/room/verify/', {
            'roomName': 'testRoom2',
            'password': 'password'
        })
        self.assertEqual(response.content, b'verified')
        response = client.post('/room/verify/', {
            'roomName': 'testRoom3',
            'password': ''
        })
        self.assertEqual(response.content, b'room is full')

    def test_quick_start(self):
        client = Client()
        response = client.get('/room/quickStart/')
        self.assertEqual(response.content, b'ws/room/testRoom')
        Room.objects.all().delete()
        response = client.get('/room/quickStart/')
        self.assertEqual(response.content, b'no suitable room')
