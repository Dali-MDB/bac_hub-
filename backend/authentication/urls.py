from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [
    path('',view=views.protected_view),
    path('register/',view=views.register),
    path('login/',view=views.login),
    path('change_password/',view=views.change_password),
    path('get_refresh/',view=views.get_refresh),
]
