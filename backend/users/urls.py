from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('profile/me/view/',view=views.view_my_profile),
    path('profile/me/update/',view=views.update_my_profile),
    path('profile/all/',view=views.get_all_profiles),
    path('profile/<int:profile_id>/',view=views.get_profile),
]


