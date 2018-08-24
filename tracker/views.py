from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Username, Task
from django.utils import dateparse
import datetime
import math


# Create your views here.

def index(request):
    return render(request, 'tracker/index.html')


def process_entry(request):
    try:
        in_username = request.POST['username']
        in_task = request.POST['task']
        if request.POST['start'] and request.POST['end']:
            # convert times to time difference in hours and minutes
            current_date = datetime.date.today()
            in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['start']))
            in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['end']))
            t = in_end - in_start
            in_hours = math.floor(t.seconds/3600)
            in_minutes = (t.seconds % 3600)/60
        else:
            in_hours = request.POST['hours']
            in_minutes = request.POST['minutes']
    except KeyError:
        return "Key does not exist"
    else:
        if Username.objects.get(username_text=in_username):
            print("username verified!")
            if Task.objects.get(task_text=in_task):
                print("task is present")
                selected_task = Task.objects.get(task_text=in_task)
                selected_task.time_set.create(time_hours = in_hours, time_minutes=in_minutes)
        return HttpResponse([in_username, in_task, in_hours, in_minutes])


def task_viewer(request, username):
    user = get_object_or_404(Username, username_text=username)
    # task_list = get_object_or_404(Task, performed_by=user)
    return render(request, 'tracker/task_viewer.html', {'user': user})

