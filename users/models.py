from django.db import models
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.
class CustomUser(AbstractUser):
    def upload_to(self, instance = None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None
    email = models.EmailField(unique=True)
    image = models.ImageField(default='default/avatar.jpg', upload_to=upload_to)

    def __str__(self):
        return self.username