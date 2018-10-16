from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, admin
from django.conf.urls import url
from django.http import HttpResponse
from .models import WorkHour, Cat, SubCat
from login.models import Employee

from django.utils import dateparse
import datetime
import math


# Create your views here.

def index(request, user):
    user_obj = Employee.objects.get(Username=user)
    cats = Cat.objects.all()
    subcats = SubCat.objects.all()
    cat_subcat = {}
    for i in cats:
        cat_subcat[str(i.Category)] = []
    for s in cats:
        for t in SubCat.objects.filter(Parent_Category=s.pk):
            cat_subcat[str(s)].append(t.SubCategory)
    return render(request, 'tracker/index.html', {'user': user, 'user_obj': user_obj, 'codes': cats, 'subcodes': subcats, 'cat_dict': cat_subcat})


def add_code(request, user):
    # New work code
    if request.POST['action'] == 'code':
        new_code = request.POST['new_code']
        new_cat = request.POST['new_cat']
        # Check if code already exists

        for entry in SubCat.objects.all():
            if entry.SubCategory == new_code:
                messages.error(request, 'This code already exists')
                return redirect('tracker:index', user=user)
    q = Cat.objects.get(Category=new_cat)
    q.subcat_set.create(Parent_Category=q.pk, SubCategory=new_code)
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
            in_subcode = request.POST['subcode']
            in_task = request.POST['task']
            in_date = request.POST['date']
            num_req = len(request.POST.dict())
            if num_req == 14:
                in_rework = True
            else:
                in_rework = False
            # Process team members
            team = []
            for i in range(1, 4):
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
                if int(in_hours) > 16:
                    messages.warning(request, 'The max number of hours is 16; go home.')
                    return redirect('tracker:index', user=user)
            else:
                in_hours = request.POST['hours']
                in_minutes = request.POST['minutes']
        except KeyError:
            return "Key does not exist"  # Any of the inputs are not available for some reason
        else:
            # Creates new entry for time record
            selected_user = Employee.objects.get(Username=user)
            selected_cat = Cat.objects.get(Category=in_code)
            selected_subcat = SubCat.objects.get(SubCategory=in_subcode, Parent_Category=selected_cat.pk)
            selected_user.workhour_set.create(Employee=selected_user.pk, Date_Worked=in_date, Task_Category=selected_subcat, Hours=in_hours, Minutes=in_minutes, Work_Description=in_task, Rework=in_rework)
            selected_user.save()
            messages.success(request, 'Task successfully saved!')
            # Creates entries for team members
            if len(team) > 0:
                for s in team:
                    selected_user = Employee.objects.get(Username=s)
                    selected_cat = Cat.objects.get(Category=in_code)
                    selected_subcat = SubCat.objects.get(SubCategory=in_subcode, Parent_Category=selected_cat.pk)
                    selected_user.workhour_set.create(Employee=selected_user.pk, Date_Worked=in_date,
                                                      Task_Category=selected_subcat, Hours=in_hours, Minutes=in_minutes,
                                                      Work_Description=in_task, Rework=in_rework)
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
            if str(entry.Task_Category) == task_name:  # and str(entry.Employee) == user
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



