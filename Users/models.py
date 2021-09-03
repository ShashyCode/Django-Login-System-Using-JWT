from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50)
    address =  models.CharField(max_length=50)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username