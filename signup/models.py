import random
import secrets
import jdatetime
import pytz
from django.db import models

# Create your models here.


def getRandomInt():
    return random.randint(12345, 99999)


def getRandomToken():
    return secrets.token_urlsafe(90)


def getDatetime():
    return jdatetime.datetime.now()


def getFakeDateTime():
    return jdatetime.datetime(1300, 1, 1)


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


class Courier(models.Model):
    SuNumber = models.IntegerField(default=getRandomInt)  # Subscription Number
    Name = models.CharField(max_length=100)
    Family = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Password = models.CharField(max_length=100, default='')
    Phone = models.CharField(max_length=13)
    CountryCode = models.IntegerField(default=98)
    Session = models.CharField(max_length=120, default=getRandomToken)
    isActive = models.BooleanField(default=False)
    BikeDeliveryCode = models.IntegerField(default=0)


class BikeDeliveryManger(models.Model):
    SuNumber = models.IntegerField(default=getRandomInt)  # Subscription Number
    Name = models.CharField(max_length=100)
    Family = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Password = models.CharField(max_length=100, default='')
    Language = models.CharField(max_length=10, default='EN')
    Phone = models.CharField(max_length=13)
    CountryCode = models.IntegerField(default=98)
    Session = models.CharField(max_length=120, default=getRandomToken)
    ImagePath = models.CharField(max_length=100, default='')
    isActive = models.BooleanField(default=False)


class BikeDelivery(models.Model):
    SuNumber = models.IntegerField(default=getRandomInt)
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=500)
    Phone = models.CharField(max_length=13)
    CountryCode = models.IntegerField(default=98)
    nCourier = models.IntegerField(default=0)
    BikeDeliveryManger = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    RegisterTime = models.DateTimeField(default=getDatetime)
    DeleteTime = models.DateTimeField(default=getFakeDateTime)


class VerifyCode(models.Model):
    Email = models.CharField(max_length=50)
    Session = models.CharField(max_length=150)
    Code = models.IntegerField(default=getRandomInt)
    Time = models.DateTimeField(default=getDatetime)
