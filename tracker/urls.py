#!/usr/bin/python
from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:user>/', views.index, name='index'),
    path('<str:user>/results/', views.process_entry, name='results'),
    path('<str:user>/code/', views.add_code, name='codes'),
    path('<str:user>/tasks/', views.task_viewer, name='tasks'),
    path('<str:user>/chart/', views.chart_data, name='chart')
]
