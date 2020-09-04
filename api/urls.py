from django.contrib import admin
from django.urls import path
from django.conf.urls import include 
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('photos', views.PhotoViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
