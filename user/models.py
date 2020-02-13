"""
database models
"""
from django.db import models


class User(models.Model):
    """
    storage users' information
    """
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class Image(models.Model):
    """
    headImage
    """
    name = models.CharField(max_length=30)
    headImage = models.ImageField(upload_to='image/')


class Hero(models.Model):
    """
    Hero files
    """
    name = models.CharField(max_length=30)
    index = models.IntegerField()
    heroImage = models.ImageField(upload_to='hero/image/')


class Counter(models.Model):
    """
    count how many heros a user has
    """
    name = models.CharField(max_length=30)
    num = models.IntegerField()
