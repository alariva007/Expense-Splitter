from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('groups_list', views.groups_list, name="groups_list"),
    path('groups_list/group_page', views.group_page, name = "group_page"),
]