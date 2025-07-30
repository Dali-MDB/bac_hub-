from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('initialize_subjects/',view=views.init_subjects),
    path('subjects/',view=views.get_all_subjects),
    path('subjects/<int:sub_id>/',view=views.get_subject),
    path('subjects/<int:sub_id>/',view=views.update_subject),
    path('subjects/<int:sub_id>/',view=views.delete_subject),
    path('subjects/field/',view=views.get_subjects_by_field),
]
