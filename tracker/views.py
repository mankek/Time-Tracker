from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task, Code
from login.models import User

from django.utils import dateparse
import datetime
import math


# Create your views here.

def index(request, in_username):
    user_obj = User.objects.get(username_text=in_username)
    codes = Code.objects.all()
    return render(request, 'tracker/index.html', {'user': in_username, 'user_obj': user_obj, 'codes': codes})


def process_entry(request, in_username):
    messages.set_level(request, messages.INFO)
    if request.POST['action'] == 'previous':
        return redirect('login:login')
    elif request.POST['action'] == 'code':
        new_code = request.POST['new_code']
        for entry in Code.objects.all():
            if entry.code_text == new_code:
                messages.error(request, 'This code already exists')
                return redirect('tracker:index', in_username=in_username)
        q = Code(code_text=new_code)
        q.save()
        return redirect('tracker:index', in_username=in_username)
    elif request.POST['action'] == 'submission':
        try:
            in_code = request.POST['code']
            in_task = request.POST['task']
            in_date = request.POST['date']
            if datetime.date(int(in_date.split("-")[0]), int(in_date.split("-")[1]), int(in_date.split("-")[2])) > datetime.date.today():
                messages.warning(request, 'You cannot input a future task!')
                return redirect('tracker:index', in_username=in_username)
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
                if str(entry.task_code) == in_code and str(entry.performed_by) == in_username:
                    print("task is present")
                    selected_user = User.objects.get(username_text=in_username)
                    selected_code = Code.objects.get(code_text=in_code)
                    selected_task = Task.objects.filter(task_code=selected_code.pk).get(performed_by=selected_user.pk)
                    selected_task.time_set.create(time_hours=in_hours, time_minutes=in_minutes, task_text=in_task, date_performed=in_date)
                    selected_task.save()
                    messages.success(request, 'Task successfully saved!')
                    return redirect('tracker:index', in_username=in_username)
                else:
                    continue
            print("new task")
            selected_user = User.objects.get(username_text=in_username)
            selected_code = Code.objects.get(code_text=in_code)
            selected_user.task_set.create(task_code=selected_code)
            selected_user.save()
            selected_task = Task.objects.filter(task_code=selected_code.pk).get(performed_by=selected_user.pk)
            selected_task.time_set.create(time_hours=in_hours, time_minutes=in_minutes, task_text=in_task, date_performed=in_date)
            selected_task.save()
            messages.success(request, 'Task successfully saved!')
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
            if str(entry.task_code) == task_name:
                tasks.append(entry)
        # task_list = get_object_or_404(Task, performed_by=user)
        return render(request, 'tracker/task_viewer.html', {'tasks': tasks, 'task': task_name, 'user': in_username})



