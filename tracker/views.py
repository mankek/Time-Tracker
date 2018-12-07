from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, admin
from django.http import JsonResponse, HttpResponse
from urllib import parse
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
            team_length = int(request.POST['team_length'])
            rework = request.POST['rework']
            if rework == "Yes":
                in_rework = True
            else:
                in_rework = False
            # Process team members
            team = []
            if team_length != 0:
                for i in range(1, team_length + 1):
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


def chart_data(request, user):
    user_obj = Employee.objects.get(Username=user)
    time_limit = request.GET.get("Time")
    response = {}
    if request.GET.get("X") == "Categories":
        for s in Cat.objects.all():
            response[s.Category] = 0
        if time_limit == "None":
            for i in user_obj.workhour_set.all():
                for t in response.keys():
                    if str(i.Task_Category).split("-")[0] == t:
                        response[t] += 1
            return JsonResponse(response)
        else:
            for i in user_obj.workhour_set.all():
                if time_check(i, time_limit):
                    for t in response.keys():
                        if str(i.Task_Category).split("-")[0] == t:
                            response[t] += 1
            return JsonResponse(response)
    elif request.GET.get("X") == "Rework":
        response = {"Rework": 0, "Not Rework": 0}
        if time_limit == "None":
            for u in user_obj.workhour_set.all():
                if u.Rework == True:
                    response["Rework"] += 1
                elif u.Rework == False:
                    response["Not Rework"] += 1
            return JsonResponse(response)
        else:
            for u in user_obj.workhour_set.all():
                if time_check(u, time_limit):
                    if u.Rework == True:
                        response["Rework"] += 1
                    elif u.Rework == False:
                        response["Not Rework"] += 1
            return JsonResponse(response)


# Function (not route) for chart_data
def time_check(entry, time):
    one_week = datetime.timedelta(days=7)
    one_month = datetime.timedelta(days=31)
    if time == "None":
        return False
    elif time == "Day":
        if entry.Date_Worked == datetime.date.today():
            return True
    elif time == "Week":
        if entry.Date_Worked >= (datetime.date.today() - one_week):
            return True
    elif time == "Month":
        if entry.Date_Worked >= (datetime.date.today() - one_month):
            return True


def task_viewer(request, user):  # task_name
    response = []
    # Control user (shouldn't ever change)
    user_obj = Employee.objects.get(Username=user)
    # Control Category
    if request.GET.get("Category") == "all":
        for i in user_obj.workhour_set.all():
            response.append(str(i.Task_Category) + ": " + str(i.Work_Description) + " - " + str(i.Hours) + " Hours and " + str(i.Minutes) + " Minutes, " + str(i.Date_Worked))
    else:
        for s in user_obj.workhour_set.all():
            if str(s.Task_Category).split("-")[0] == request.GET.get("Category"):
                response.append(
                    str(s.Task_Category) + ": " + str(s.Work_Description) + " - " + str(s.Hours) + " Hours and " + str(
                        s.Minutes) + " Minutes, " + str(s.Date_Worked))
            else:
                continue
    # Control SubCategory
    if request.GET.get("Subcategory") == "all":
        return JsonResponse(response, safe=False)
    else:
        response = noncat_control(request.GET.get("Subcategory"), "Subcategory", response)
        return JsonResponse(response, safe=False)


def noncat_control(req, req_type, response):
    if req_type == "Subcategory":
        for t in response:
            if t.split(":")[0].split("-")[1] != req:
                response.remove(t)
                noncat_control(req, req_type, response)
            else:
                continue
        return response










