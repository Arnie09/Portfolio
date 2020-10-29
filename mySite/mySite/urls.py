from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views
from blog import views as blog_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),

    #user signups
    path('user/signup', user_views.signup, name='signup'),
    path('user/signin', user_views.signin, name='signin'),
    path('user/signout', user_views.signout, name='signout'),
    
    #blogs
    path('blog/<slug:slug>/', blog_views.blogs.as_view(), name='blogs'),
    path('blog_detail/<slug:slug>/', blog_views.PostDetail.as_view(), name='post_detail'),
    path('blog/like_post', blog_views.like_post, name='like_blogs'),
    path('blog/unlike_post', blog_views.unlike_post, name='unlike_blogs'),
    path('blog/create_post', blog_views.create_post, name='create_post'),
    path('blog/edit_post/<slug:slug>/', blog_views.edit_post, name='edit_post'),
    path('blog/delete_post/<slug:slug>/', blog_views.delete_post, name='delete_post'),

    #user
    path('profile/', user_views.MyProfile.as_view(), name='my_profile')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
