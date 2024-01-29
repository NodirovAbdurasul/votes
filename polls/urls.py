from django.contrib import admin
from django.urls import path
from .views import index, registration,login, votes

urlpatterns = [
    path("polls/", index, name="index"),
    path('', registration, name="registration"),
    path("login/", login, name="login"),
    path("voting/", votes, name="voting")
]