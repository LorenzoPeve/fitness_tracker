from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    dob = models.DateField()
    email = models.EmailField(max_length=50)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
