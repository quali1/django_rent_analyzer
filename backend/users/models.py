from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from analyzer.models import Offer



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_offers = models.ManyToManyField(Offer, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"
