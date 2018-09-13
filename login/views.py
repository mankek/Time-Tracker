from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(request):
    return render(request, 'login/index.html')


def new(request):
    new_first = request.POST['new_first']
    new_last = request.POST['new_last']
    new_user = request.POST['new_user']
    depart = request.POST['department']
    role = request.POST['role']
    # Check that the username is not in use
    for entry in User.objects.all():
        if entry.username_text == new_user:
            messages.error(request, 'This username is already taken')
            return redirect('login:login')
    # Create new user
    q = User(first_name=new_first, last_name=new_last, username_text=new_user,
             department=depart, role=role)
    q.save()
    return redirect('tracker:index', in_username=new_user)


def logged(request):
    u_name = request.POST['return_user']
    # Check that user exists
    try:
        User.objects.get(username_text=u_name)
    except:
        messages.error(request, 'This user does not exist')
        return redirect('login:login')
    return redirect('tracker:index', in_username=u_name)
