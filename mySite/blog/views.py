from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from user.forms import CreateUserForm
from django.contrib.auth.models import AnonymousUser
from .models import BlogPost, BlogLikes, Category
from user.models import ExtendedUser
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib import messages

from .forms import FormPost

# Create your views here.
class blogs(ListView):

    model = BlogPost
    queryset = None
    paginate_by = 5
    context_object_name = 'blogs'
    template_name = 'mySite/blog_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = BlogPost.objects.filter(reviewed = True).order_by('-date')

        category = self.kwargs.get("slug", None)
        print("Category is: ", category)
        if (category != 'index'):
            categoryObj = Category.objects.get(title = category)
            print("category is: ",str(categoryObj))
            qs = qs.filter(tags = categoryObj)

        return qs

    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        context['signout'] = 0 if self.request.user.is_anonymous else 1
        context['likes'] = {}
        register_form = CreateUserForm()
        context['form_register'] = register_form
        for blogs in BlogPost.objects.filter():
            context['likes'][blogs.slug] = BlogLikes.objects.filter(blog_id = blogs).count()
        
        context['topthree'] = BlogPost.objects.filter(reviewed = True).order_by('-views')[:3]
        

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

        return render(response, self.template_name, {'likes': additional_info, 'object': blogObj, 'liked': like_state})

def like_post(request):
    if request.method == "POST":
        blog_id = request.POST.get('payload[blog_id]')
        user = request.user
        
        blogObj = BlogPost.objects.get(blog_id = blog_id)
        BlogLikes.objects.create(blog_id = blogObj, user = user)

        likes = BlogLikes.objects.filter(blog_id = blogObj).count()

        print("Like was called!")
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

def create_post(request):

    form = FormPost(request.POST or None)

    if request.method == 'POST':
        
        try:
            if (form.is_valid()):
                user = request.user
                extendedUser = ExtendedUser.objects.get(user = user)
                obj = form.save(commit=False)
                obj.authorUser = user
                if (extendedUser.canPost):
                    obj.reviewed = True
                obj.save()
                messages.success(request, "Post successfully saved!")
                form = FormPost()
            else:
                messages.error(request, form.errors)

        except Exception as e:
            print(e)
            messages.error(request, "Error saving this blog post! {}".format(e))

    context = {
        'form': form
    }
    return render(request, 'mySite/create_post.html', context)


def edit_post(request, slug = None):

    if request.method == 'GET':
        blog = BlogPost.objects.get(slug = slug)
        print(blog)
        form = FormPost(instance=blog)

        

    elif request.method == 'POST':

        form = FormPost(request.POST)
        try:
            if (form.is_valid()):
                print("Here asdasdasd")
                user = request.user
                slug = form.cleaned_data.get('slug')
                print("haghsahbd",slug)
                blog = BlogPost.objects.filter(slug = slug)
                blog.title = form.cleaned_data.get('title')

                messages.success(request, "Post successfully saved!")
                form = FormPost()
            else:
                messages.error(request, form.errors)

        except Exception as e:
            print(e)
            messages.error(request, "Error saving this blog post! {}".format(e))


    context = {
        'form': form,
        'edit':1
    }
    return render(request, 'mySite/create_post.html', context)


def delete_post(request, slug = None):

    if request.method == "GET":
        blog = BlogPost.objects.get(slug = slug)
        author = blog.authorUser
        user = request.user

        if (author == user):
            blog.delete()

        response = {
        }

        return JsonResponse(response)

    return redirect('/')