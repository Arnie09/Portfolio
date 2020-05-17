from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import json

from blog.models import BlogPost

def index(request):
    posts = BlogPost.objects.filter().order_by('-date')[:5]
    recent_posts = {
        'blogs':posts
    }
    return render(request, 'mySite/index.html', recent_posts)