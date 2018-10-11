from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, admin
from django.conf.urls import url
from django.http import HttpResponse
from .models import WorkHour, WorkCode
from login.models import Employee

from django.utils import dateparse
import datetime
import math


# Create your views here.

def index(request, user):
    user_obj = Employee.objects.get(Username=user)
    codes = WorkCode.objects.all()
    return render(request, 'tracker/index.html', {'user': user, 'user_obj': user_obj, 'codes': codes})


def add_code(request, user):
    # New work code
    # Logout button
    if request.POST['action'] == 'code':
        new_code = request.POST['new_code']
        # Check if billable checkbox is checked
        bill = request.POST.dict()
        if len(bill) > 3:
            billable = True
        elif len(bill) == 3:
            billable = False
        # Check if code already exists
        for entry in WorkCode.objects.all():
            if entry.Description == new_code:
                messages.error(request, 'This code already exists')
                return redirect('tracker:index', user=user)
    q = WorkCode(Description=new_code, Billable=billable)
    q.save()
    return redirect('tracker:index', user=user)


def process_entry(request, user):
    messages.set_level(request, messages.INFO)
    # Logout button
    if request.POST['action'] == 'previous':
        return redirect('login:login')
    # New time record
    elif request.POST['action'] == 'submission':
        try:
            in_code = request.POST['code']
            in_task = request.POST['task']
            in_date = request.POST['date']
            # Process team members
            team = []
            num_team = len(request.POST.dict())-9
            if num_team > 0:
                for i in range(1, num_team + 1):
                    if request.POST['team' + str(i)] != "none":
                        team.append(request.POST['team' + str(i)])
            # Process time
            if datetime.date(int(in_date.split("-")[0]), int(in_date.split("-")[1]), int(in_date.split("-")[2])) > datetime.date.today():
                messages.warning(request, 'You cannot input a future task!')
                return redirect('tracker:index', user=user)
            if request.POST['start'] and request.POST['end']:
                # convert times to time difference in hours and minutes
                current_date = datetime.date.today()
                in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['start']))
                in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['end']))
                t = in_end - in_start
                in_hours = math.floor(t.seconds/3600)
                tot_minutes = (t.seconds % 3600)/60
                quarters = math.floor(tot_minutes/15)
                in_minutes = quarters * 15
                if int(in_hours) > 10:
                    messages.warning(request, 'The max number of hours is 10; go home.')
                    return redirect('tracker:index', user=user)
            else:
                in_hours = request.POST['hours']
                in_minutes = request.POST['minutes']
        except KeyError:
            return "Key does not exist"  # Any of the inputs are not available for some reason
        else:
            # Creates new entry for time record
            selected_user = Employee.objects.get(Username=user)
            selected_code = WorkCode.objects.get(Description=in_code)
            selected_user.workhour_set.create(Employee=selected_user.pk, Date_Worked=in_date, Work_Code=selected_code, Hours=in_hours, Minutes=in_minutes, Work_Description=in_task)
            selected_user.save()
            messages.success(request, 'Task successfully saved!')
            # Creates entries for team members
            if len(team) > 0:
                for s in team:
                    selected_user = Employee.objects.get(Username=s)
                    selected_code = WorkCode.objects.get(Description=in_code)
                    selected_user.workhour_set.create(Employee=selected_user.pk, Date_Worked=in_date,
                                                      Work_Code=selected_code, Hours=in_hours, Minutes=in_minutes,
                                                      Work_Description=in_task)
                    selected_user.save()
                    messages.success(request, 'Team member successfully updated!')
            return redirect('tracker:index', user=user)


def task_viewer(request, user, task_name):
    # Redirection buttons
    if request.method == 'POST':
        if request.POST['action'] == 'previous':
            return redirect('login:login')
        elif request.POST['action'] == 'home':
            return redirect('tracker:index', user=user)
    else:
        # List of task details
        tasks = []
        for entry in WorkHour.objects.all():
            if str(entry.Work_Code) == task_name:
                tasks.append(entry)
        # task_list = get_object_or_404(Task, performed_by=user)
        return render(request, 'tracker/task_viewer.html', {'tasks': tasks, 'task': task_name, 'user': user})


# def my_view(request):
#     return render(request, 'tracker/ad_option.html')
#
#
# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = [
#             url(r'^my_view/$', admin.site.admin_view(my_view))
#         ]
#         return my_urls + urls
#     return get_urls
#
#
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls



