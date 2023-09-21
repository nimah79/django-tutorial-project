"""spotify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from spotify.views import author_posts, ContactFormView, CreatePostView, login, signup, UserCreateView, UserDeleteView, UserDetailView, UserListView, UserUpdateView, hello, index, post_details, posts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('posts/<int:id>/', post_details),
    path('posts', posts),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('users', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete', UserDeleteView.as_view(), name='user-delete'),
    path('users/new', UserCreateView.as_view()),
    path('create_post', CreatePostView.as_view()),
    path('contact', ContactFormView.as_view()),
    path('authors/<int:id>/posts', author_posts),
    path('<str:name>/<int:number>/', index),
    path('__debug__/', include('debug_toolbar.urls')),
]
