from django.db import models
from django.contrib.auth.models import User

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canPost = models.BooleanField(default = False)
    points = models.IntegerField(null=False, default = 0)