from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.email})"
