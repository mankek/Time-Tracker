from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee


# renders the login screen
def index(request):
    return render(request, 'login/index.html')


# checks that the input username and password are correct
def logged(request):
    user = request.POST['in_user']
    password = request.POST['in_pass']
    # Check that the username is not in use
    for entry in Employee.objects.all():
        if entry.Username == user and entry.Password == password:
            return redirect('tracker:index', user=user)
    messages.error(request, 'Employee not found; make sure your employee information has been added to the database.')
    return redirect('login:login')




