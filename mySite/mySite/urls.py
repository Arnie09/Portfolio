from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views
from blog import views as blog_views
from comments import views as comment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('accounts/', include('allauth.urls')),
    path('blog/', blog_views.blogs.as_view(), name='blogs'),
    path('blog/<slug:slug>/', blog_views.PostDetail.as_view(), name='post_detail'),
    path('blog/like_post', blog_views.like_post, name='like_blogs'),
    path('blog/unlike_post', blog_views.unlike_post, name='unlike_blogs'),
    path('blog/add_comment', comment_views.add_comment, name='add_comment'),
    path('blog/delete_comment', comment_views.delete_comment, name='delete_comment'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
