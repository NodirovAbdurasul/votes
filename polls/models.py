from django.db import models

from users.models import MyUser


# Create your models here.


class Vote(models.Model):
    VOTE_CHOICES = (
        ('d', 'democrats'),
        ('r', 'respublicans'),
    )
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    vote_to = models.CharField(max_length=1, choices=VOTE_CHOICES)