from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='login'),
    path('created/', views.new, name='new'),
    path('logged_in/', views.logged, name='logged')
]
