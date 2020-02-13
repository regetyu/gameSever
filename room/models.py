from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=30)
    cur_num = models.IntegerField()
    max_num = models.IntegerField()
    game_map = models.IntegerField()
    player1 = models.CharField(max_length=30)
    player2 = models.CharField(max_length=30)
    player3 = models.CharField(max_length=30)
    player4 = models.CharField(max_length=30)
    ready2 = models.IntegerField()
    ready3 = models.IntegerField()
    ready4 = models.IntegerField()
    hasPassword = models.IntegerField()
    password = models.CharField(max_length=30)
    readyNum = models.IntegerField()
