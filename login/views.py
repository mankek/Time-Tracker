from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .models import Employee


# Create your views here.
def index(request):
    return render(request, 'login/index.html')


def logged(request):
    user = request.POST['in_user']
    password = request.POST['in_pass']
    # Check that the username is not in use
    for entry in Employee.objects.all():
        if entry.Username == user and entry.Password == password:
            return redirect('tracker:index', user=user)
    messages.error(request, 'Employee not found; make sure your employee information has been added to the database.')
    return redirect('login:login')




