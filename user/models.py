from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField("Phone Number", null=True, blank=True)
    location = models.CharField("Location", max_length=100)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username + " : " + self.email
