import random
import secrets
import jdatetime
from django.db import models

# Create your models here.


def getRandomInt():
    return random.randint(12345, 99999)


def getRandomToken():
    return secrets.token_urlsafe(100)


def getDatetime():
    return str(jdatetime.datetime.today())


class Customer(models.Model):
    genderChoices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    SuNumber = models.IntegerField(default=getRandomInt)  # Subscription Number
    Name = models.CharField(max_length=100)
    Family = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Password = models.CharField(max_length=100, default='')
    Phone = models.CharField(max_length=13)
    CountryCode = models.IntegerField(default=98)
    Gender = models.CharField(max_length=7, choices=genderChoices)
    Session = models.CharField(max_length=120, default=getRandomToken)
    isActive = models.BooleanField(default=False)


class VerifyCode(models.Model):
    Email = models.CharField(max_length=50)
    Session = models.CharField(max_length=150)
    Code = models.IntegerField(default=getRandomInt)
    Time = models.DateTimeField(default=getDatetime)
