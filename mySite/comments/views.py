from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog.models import BlogPost, BlogLikes
from .models import Comments
from datetime import datetime

# Create your views here.
def add_comment(request):

    if request.method == "POST":
        user = request.user
        blog_id = request.POST.get('payload[blog_id]')
        comment_text = request.POST.get('payload[text]')
        blog_post = BlogPost.objects.get(blog_id = blog_id)

        comment_obj = Comments(
            post = blog_post,
            author = user,
            text = comment_text,
            date = datetime.now()
        )

        comment_obj.save()

        response = {
            'success': 4
        }

        return JsonResponse(response)


    return redirect('/')


def delete_comment(request):
    
    if request.method == "POST":
        user = request.user
        comment_id = request.POST.get('payload[comment_id]')
        Comments.objects.get(comment_id = comment_id).delete()

        response = {
            'success': 4
        }

        return JsonResponse(response)


    return redirect('/')