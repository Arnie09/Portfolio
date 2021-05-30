from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import ExtendedUser

from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.generic.list import ListView

from .forms import CreateUserForm
from blog.models import BlogPost

def signup(request):
    if request.method == "POST":
        print("We here! ", request.method)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if (password != password2):
                messages.error(request, "Passwords dont match!")
                return redirect('blogs')

            try:              
                user = authenticate(username=username, password=password)
                login(request, user)

                extended_userobj = ExtendedUser(user = user)
                extended_userobj.save()
                messages.success(request, 'Successfully created account!')
                return redirect('blogs', slug = "index")
            except:
                messages.error(request, 'Email/Username exists')
                return redirect('blogs', slug = "index")
        else:
            print(form.error_messages)
            return redirect('blogs', slug = "index")
    else:
        return redirect('blogs', slug = "index")
    



def signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user =  authenticate(username = username,password = password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect('blogs', slug = "index")  
        else:
            messages.error(request, "Failed to Log In!")
            return redirect('blogs', slug = "index")

        

def signout(request):
    logout(request)
    return redirect('blogs', slug = "index")


class MyProfile(ListView):

    template_name = 'mySite/profile.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(reviewed = True, authorUser = self.request.user)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.is_anonymous)
        if self.request.user.is_anonymous:
            context['display'] = 0
        else:
            context['display'] = 1
            extended_user_obj = ExtendedUser.objects.filter(user = self.request.user)
            print(extended_user_obj)
            if len(extended_user_obj) == 0:
                extended_user_obj = ExtendedUser(user = self.request.user)
                extended_user_obj.save()
            else:
                extended_user_obj = extended_user_obj[0]
            context['additional_info'] = extended_user_obj
            context['your_blogs'] = BlogPost.objects.filter(reviewed = True, authorUser = self.request.user)

        return context