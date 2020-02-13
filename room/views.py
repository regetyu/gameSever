from django.shortcuts import render
from django.http import HttpResponse
from room.models import Room

"""
views
"""


def creat_room(request):
    if request.POST:
        room_name = request.POST['roomName']
        max_num = request.POST['max']
        hasPassword = request.POST['hasPassword']
        password = request.POST['password']
        try:
            if Room.objects.get(name=room_name):
                return HttpResponse('room already exists')
        except Room.DoesNotExist:
            pass
        Room.objects.create(
            name=room_name,
            cur_num=0,
            max_num=max_num,
            game_map=0,
            ready2=0,
            ready3=0,
            ready4=0,
            password=password,
            hasPassword=hasPassword,
            readyNum=0
        )
        return HttpResponse('create room success')
    return HttpResponse('not post request')


def get_all_room(request):
    string = []
    for room in Room.objects.all():
        string.append(room.name + '\n' + str(room.cur_num) + '\n' + str(
            room.max_num) + '\n' + str(room.game_map) + '\n' + room.player1 +
                      '\n' + room.player2 + '\n' + room.player3 + '\n' +
                      room.player4 + '\n' + str(room.hasPassword) + '\n\t')
    return HttpResponse(string)


def get_single_room(request):
    if request.POST:
        room_name = request.POST['roomName']
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return HttpResponse('room does not exist')
        return HttpResponse(room.name + '\n' + str(room.cur_num) + '\n' +
                            str(room.max_num) + '\n' + str(room.game_map) +
                            '\n' + room.player1 + '\n' + room.player2 + '\n' +
                            room.player3 + '\n' + room.player4 + '\n' +
                            str(room.ready2) + '\n' + str(room.ready3) + '\n'
                            + str(room.ready4) + '\n' + str(room.hasPassword)
                            + '\n\t')
    return HttpResponse('not post request')


def verify(request):
    if request.POST:
        room_name = request.POST['roomName']
        password = request.POST['password']
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return HttpResponse('room does not exist')
        if room.hasPassword == 1 and room.password != password:
            return HttpResponse('password incorrect')
        if room.cur_num + 1 > room.max_num:
            return HttpResponse('room is full')
        return HttpResponse('verified')
    return HttpResponse('not post request')


def quick_start(request):
    for room in Room.objects.all():
        if room.cur_num + 1 <= room.max_num:
            return HttpResponse('ws/room/' + room.name)
    return HttpResponse('no suitable room')


def get_all_player(request):
    string = []
    for room in Room.objects.filter(hasPassword=0):
        cur_num = room.cur_num
        if cur_num == 1:
            string.append(room.player1 + '\n')
        elif cur_num == 2:
            string.append(room.player1 + '\n' + room.player2 + '\n')
        elif cur_num == 3:
            string.append(room.player1 + '\n' + room.player2 + '\n' +
                          room.player3 + '\n')
        elif cur_num == 4:
            string.append(room.player1 + '\n' + room.player2 + '\n' +
                          room.player3 + '\n' + room.player4)
    return HttpResponse(string)
