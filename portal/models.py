from django.db import models
from signup.models import getRandomInt,\
    getDatetime, getFakeDateTime
# Create your models here.


class Requests(models.Model):
    Code = models.IntegerField(default=getRandomInt)
    CourierCode = models.IntegerField(default=0)
    BikeDeliveryCode = models.IntegerField(default=0)
    RegisterTime = models.DateTimeField(default=getDatetime)
    ActionTime = models.DateTimeField(default=getFakeDateTime)
    Status = models.BooleanField(blank=True)
    isChecked = models.BooleanField(default=False)



