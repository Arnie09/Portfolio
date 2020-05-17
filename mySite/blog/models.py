from django.db import models
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.
class BlogPost(models.Model):
    blog_id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    title = models.CharField(max_length = 256, null = False)
    slug = models.SlugField(unique = True, null = False)
    image = models.URLField(null = False)
    author = models.CharField(max_length = 256, null = False)
    content = models.TextField()
    time = models.IntegerField(null = False)
    date = models.DateField(null = False)
    views = models.IntegerField(editable=False, default = 0)

class BlogLikes(models.Model):
    blog_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        unique_together = ('blog_id', 'user')
