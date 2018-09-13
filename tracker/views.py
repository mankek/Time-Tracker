from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task
from login.models import User

from django.utils import dateparse
import datetime
import math


# Create your views here.

def index(request, in_username):
    user_obj = User.objects.get(username_text=in_username)
    return render(request, 'tracker/index.html', {'user': in_username, 'user_obj': user_obj})


def process_entry(request, in_username):
    if request.POST['action'] == 'previous':
        return redirect('login:login')
    elif request.POST['action'] == 'submission':
        try:
            in_task = request.POST['task']
            if request.POST['start'] and request.POST['end']:
                # convert times to time difference in hours and minutes
                current_date = datetime.date.today()
                in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['start']))
                in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['end']))
                t = in_end - in_start
                in_hours = math.floor(t.seconds/3600)
                in_minutes = (t.seconds % 3600)/60
                if int(in_hours) > 9:
                    messages.warning(request, 'The max number of hours is 9; go home.')
                    return redirect('tracker:index', in_username=in_username)
            else:
                in_hours = request.POST['hours']
                in_minutes = request.POST['minutes']
        except KeyError:
            return "Key does not exist"
        else:
            # try:
            for entry in Task.objects.all():
                if str(entry.task_text) == in_task and str(entry.performed_by) == in_username:
                    print("task is present")
                    selected_user = User.objects.get(username_text=in_username)
                    selected_task = Task.objects.filter(task_text=in_task).get(performed_by=selected_user.pk)
                    selected_task.time_set.create(time_hours=in_hours, time_minutes=in_minutes)
                    selected_task.save()
                    messages.success(request, 'Task successfully saved!')
                    return redirect('tracker:index', in_username=in_username)
                else:
                    continue
            print("new task")
            selected_user = User.objects.get(username_text=in_username)
            selected_user.task_set.create(task_text=in_task)
            selected_user.save()
            selected_task = Task.objects.filter(task_text=in_task).get(performed_by=selected_user.pk)
            selected_task.time_set.create(time_hours=in_hours, time_minutes=in_minutes)
            selected_task.save()
            return redirect('tracker:index', in_username=in_username)


def task_viewer(request, in_username, task_name):
    if request.method == 'POST':
        if request.POST['action'] == 'previous':
            return redirect('login:login')
        elif request.POST['action'] == 'home':
            return redirect('tracker:index', in_username=in_username)
    else:
        tasks = []
        for entry in Task.objects.all():
            if entry.task_text == task_name:
                tasks.append(entry)
        # task_list = get_object_or_404(Task, performed_by=user)
        return render(request, 'tracker/task_viewer.html', {'tasks': tasks, 'task': task_name})



