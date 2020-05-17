from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AnonymousUser
from .models import BlogPost, BlogLikes
from django.views.generic.list import ListView
from django.views.generic import DetailView


# Create your views here.
class blogs(ListView):

    queryset = BlogPost.objects.filter().order_by('-date')
    paginate_by = 5
    context_object_name = 'blogs'
    template_name = 'mySite/blog_list.html'

    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        context['signout'] = 0 if self.request.user.is_anonymous else 1
        return context


class PostDetail(DetailView):
    model = BlogPost
    template_name = 'mySite/blog_post.html'

    def get(self, response, *args, **kwargs):
        slug = self.kwargs['slug']
        blogObj = BlogPost.objects.get(slug = slug)
        blogObj.views+=1
        blogObj.save()

        additional_info = BlogLikes.objects.filter(blog_id = blogObj).count()
        like_state = -1
        if response.user.is_anonymous:
            like_state = -1
        else:
            like_state = 0 if BlogLikes.objects.filter(blog_id = blogObj, user = response.user).count() == 0 else 1

        print("Here: ",additional_info)

        return render(response, self.template_name, {'likes': additional_info, 'object': blogObj, 'liked': like_state})

def like_post(request):
    if request.method == "POST":
        blog_id = request.POST.get('payload[blog_id]')
        user = request.user
        
        blogObj = BlogPost.objects.get(blog_id = blog_id)
        BlogLikes.objects.create(blog_id = blogObj, user = user)

        likes = BlogLikes.objects.filter(blog_id = blogObj).count()

        response = {
            'likes': likes 
        }

        return JsonResponse(response)

    return redirect('/')


def unlike_post(request):
    if request.method == "POST":
        blog_id = request.POST.get('payload[blog_id]')
        user = request.user
        
        blogObj = BlogPost.objects.get(blog_id = blog_id)
        likeObj = BlogLikes.objects.filter(blog_id = blogObj, user = user)

        if len(likeObj) != 0:
            likeObj = likeObj[0]
            likeObj.delete()

        likes = BlogLikes.objects.filter(blog_id = blogObj).count()
        print("unlike was called!")

        response = {
            'likes': likes 
        }

        return JsonResponse(response)

    return redirect('/')