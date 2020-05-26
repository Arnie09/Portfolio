from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from blog.models import BlogPost

# Create your models here.
class Comments(models.Model):

    comment_id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    date = models.DateTimeField(null = False)



