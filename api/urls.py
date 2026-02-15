from django.urls import path
from .views import chat, login, register, usage

urlpatterns = [
    path("chat/", chat),
    path("login/", login),
    path("register/", register),
    path("usage/", usage),
]
