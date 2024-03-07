from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    article_id = models.IntegerField()
    price = models.IntegerField()
    price_per_sqm = models.IntegerField()
    district = models.CharField(max_length=100)
    rooms = models.IntegerField()
    area = models.FloatField()
    floor = models.IntegerField()
    link = models.URLField()

    def __str__(self):
        return f"Offer {self.id}"


class OtodomData(models.Model):
    request_id = models.CharField(max_length=16, unique=True, primary_key=True)
    offers = models.ManyToManyField(Offer)
    ai_response = models.TextField(null=True, blank=True)
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    site = models.CharField(max_length=32, default="None")
    method = models.CharField(max_length=124, default="None")

    def __str__(self):
        return f'{self.created} {self.method} {self.requester} ID: {self.request_id}'
