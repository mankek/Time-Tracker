#!/usr/bin/python
from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:in_username>/', views.index, name='index'),
    path('<str:in_username>/results/', views.process_entry, name='results'),
    path('<str:in_username>/<str:task_name>/', views.task_viewer, name='tasks')
]
