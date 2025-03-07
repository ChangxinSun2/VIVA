from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class ShowInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    ticket_link = models.URLField()

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(ShowInfo, on_delete=models.CASCADE)
