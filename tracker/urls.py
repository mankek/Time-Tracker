#!/usr/bin/python
from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.process_entry, name='results'),
    path('<str:task_name>/', views.task_viewer, name='tasks')
]
