from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")

    def __str__(self):
        return self.title

# Create your models here.
class BlogPost(models.Model):

    blog_id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    authorUser = models.ForeignKey(User, null = False, on_delete=models.CASCADE)
    title = models.CharField(max_length = 256, null = False)
    short_desc = models.CharField(max_length = 512, default = "This is a default description")
    slug = models.SlugField(unique = True, null = False)
    image = models.URLField(null = False)
    author = models.CharField(max_length = 256, null = False)
    content = models.TextField()
    time = models.IntegerField(null = False)
    date = models.DateField(null = False)
    views = models.IntegerField(editable=False, default = 0)
    tags = models.ForeignKey(Category, verbose_name = "Category", on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False, null = False)

    def save(self, *args, **kwargs):
        self.slug = self.slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)


    def slugify(self, title):
        slug = ""
        for c in title:
            if ord(c) >= 97 and ord(c) <= 122:
                slug+=c 
            elif ord(c) >= 65 and ord(c) <= 90:
                slug+=c 
            elif ord(c) >= 48 and ord(c) <= 57:
                slug+=c 
            else:
                slug+='-'

        slug.strip()
        return slug

class BlogLikes(models.Model):
    blog_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        unique_together = ('blog_id', 'user')


