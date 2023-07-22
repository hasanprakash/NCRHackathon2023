from django.contrib import admin
from django.urls import path

from .views import PostViewSet

urlpatterns = [
    path('post/', PostViewSet.as_view(), name='post')
]