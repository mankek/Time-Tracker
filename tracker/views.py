from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, admin
from django.http import JsonResponse, HttpResponse
from .models import Cat, SubCat
from login.models import Employee
from django.utils import dateparse
import datetime
import math


# gathers all the necessary profile data
def index(request, user):
    # get all employees
    employees = dict()
    for u in Employee.objects.all():
        employees[str(u.Username)] = str(u.First_Name) + " " + str(u.Last_Name)
    # get the user employee
    user_obj = Employee.objects.get(Username=user)
    # get all categories
    cats = Cat.objects.all()
    # get all subcategories
    subcats = SubCat.objects.all()
    # stores categories and their associated subcategories in a dictionary
    cat_subcat = {}
    for i in cats:
        cat_subcat[str(i.Category)] = []
    for s in cats:
        for t in SubCat.objects.filter(Parent_Category=s.pk):
            cat_subcat[str(s)].append(t.SubCategory)
    return render(request, 'tracker/index.html', {'user': user, 'codes': cats, 'subcodes': subcats, 'cat_dict': cat_subcat, 'employees': employees, 'user_obj': user_obj})


# New work code (subcategory)
def add_code(request, user):
    if request.POST['action'] == 'code':
        new_code = request.POST['new_code']
        new_cat = request.POST['new_cat']
        # Check if code already exists
        for entry in SubCat.objects.all():
            if entry.SubCategory == new_code:
                messages.error(request, 'This code already exists')
                return redirect('tracker:index', user=user)
    # gets category new code belongs to and creates new code
    q = Cat.objects.get(Category=new_cat)
    q.subcat_set.create(Parent_Category=q.pk, SubCategory=new_code)
    q.save()
    return redirect('tracker:index', user=user)


# process time entries
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
            # if the user selected start and end times
            if request.POST['start'] and request.POST['end']:
                # convert start & end times to time difference in hours and minutes
                current_date = datetime.date.today()
                in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['start']))
                in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['end']))
                t = in_end - in_start
                in_hours = math.floor(t.seconds/3600)
                tot_minutes = (t.seconds % 3600)/60
                quarters = math.floor(tot_minutes/15)
                in_minutes = quarters * 15
                # defines max number of hours that can be worked for a single task
                if int(in_hours) > 16:
                    messages.warning(request, 'The max number of hours is 16; go home.')
                    return redirect('tracker:index', user=user)
            # if the user selected hours and minutes duration
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


# processes chart data
def chart_data(request, user):
    # get the user employee
    user_obj = Employee.objects.get(Username=user)
    time_limit = request.GET.get("Time")
    response = {}
    # if the tasks should be arranged by category
    if request.GET.get("X") == "Categories":
        # initialize count for each category
        for s in Cat.objects.all():
            response[s.Category] = 0
        # if no time restriction selected, use all tasks
        if time_limit == "None":
            # for each task category increment the category count
            for i in user_obj.workhour_set.all():
                for t in response.keys():
                    if str(i.Task_Category).split("-")[0] == t:
                        response[t] += 1
            return JsonResponse(response)
        # if a time restriction is selected
        else:
            # for each task category within the time criteria increment the category count
            for i in user_obj.workhour_set.all():
                if time_check(i, time_limit):
                    for t in response.keys():
                        if str(i.Task_Category).split("-")[0] == t:
                            response[t] += 1
            return JsonResponse(response)
    # if the tasks should be arranged by rework status
    elif request.GET.get("X") == "Rework":
        response = {"Rework": 0, "Not Rework": 0}
        # if no time restriction selected, use all tasks
        if time_limit == "None":
            # for each task rework status increment the rework status count
            for u in user_obj.workhour_set.all():
                if u.Rework == True:
                    response["Rework"] += 1
                elif u.Rework == False:
                    response["Not Rework"] += 1
            return JsonResponse(response)
        # if a time restriction is selected
        else:
            # for each task rework status within the time criteria increment the rework status count
            for u in user_obj.workhour_set.all():
                if time_check(u, time_limit):
                    if u.Rework == True:
                        response["Rework"] += 1
                    elif u.Rework == False:
                        response["Not Rework"] += 1
            return JsonResponse(response)
    # if the tasks should be arranged by amount of time spent on tasks
    elif request.GET.get("X") == "Time_Spent":
        response = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
        # if no time restriction selected, use all tasks
        if time_limit == "None":
            # for each task duration increment the appropriate time slot
            for v in user_obj.workhour_set.all():
                task_hours = int(v.Hours)
                task_minutes = int(v.Minutes)
                if (task_hours < 2) or (task_hours == 2 and task_minutes == 0):
                    response["0-2"] += 1
                elif (2 < task_hours < 4) or (task_hours == 2 and task_minutes > 0) or (task_hours == 4 and task_minutes == 0):
                    response["2-4"] += 1
                elif (4 < task_hours < 6) or (task_hours == 4 and task_minutes > 0) or (task_hours == 6 and task_minutes == 0):
                    response["4-6"] += 1
                elif (6 < task_hours < 8) or (task_hours == 6 and task_minutes > 0) or (task_hours == 8 and task_minutes == 0):
                    response["6-8"] += 1
                elif (8 < task_hours) or (task_hours == 8 and task_minutes > 0):
                    response["8-10"] += 1
            return JsonResponse(response)
        # if a time restriction is selected
        else:
            # for each tasks duration that fits the time criteria increment the appropriate time slot
            for v in user_obj.workhour_set.all():
                if time_check(v, time_limit):
                    task_hours = int(v.Hours)
                    task_minutes = int(v.Minutes)
                    if (task_hours < 2) or (task_hours == 2 and task_minutes == 0):
                        response["0-2"] += 1
                    elif (2 < task_hours < 4) or (task_hours == 2 and task_minutes > 0) or (task_hours == 4 and task_minutes == 0):
                        response["2-4"] += 1
                    elif (4 < task_hours < 6) or (task_hours == 4 and task_minutes > 0) or (task_hours == 6 and task_minutes == 0):
                        response["4-6"] += 1
                    elif (6 < task_hours < 8) or (task_hours == 6 and task_minutes > 0) or (task_hours == 8 and task_minutes == 0):
                        response["6-8"] += 1
                    elif (8 < task_hours < 10) or (task_hours == 8 and task_minutes > 0) or (task_hours == 10 and task_minutes == 0):
                        response["8-10"] += 1
            return JsonResponse(response)


# Function (not route) for chart_data
# checks if a task falls within a certain time interval
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


# returns task history
def task_viewer(request, user):
    response = []
    user_obj = Employee.objects.get(Username=user)
    # for each task under the user, if the task meets the criteria add it to the response list
    for i in user_obj.workhour_set.all():
        if cat_control(request.GET.get("Category"), i):
            if subcat_control(request.GET.get("Subcategory"), i):
                if date_control(request.GET.get("Date"), i, request.GET.get("Range")):
                    response.append(str(i.Task_Category) + ": " + str(i.Work_Description) + " - " + str(i.Hours) + " Hours and " + str(i.Minutes) + " Minutes, " + str(i.Date_Worked))
                else:
                    continue
            else:
                continue
        else:
            continue
    return JsonResponse(response, safe=False)


# determines whether a task is under a certain category
def cat_control(req, user_object):
    if req == "all":
        return True
    else:
        if str(user_object.Task_Category).split("-")[0] == req:
                return True
        else:
            return False


# determines whether a task is under a certain subcategory
def subcat_control(req, user_object):
    if req == "all":
        return True
    else:
        if str(user_object.Task_Category).split("-")[-1] == req:
            return True
        else:
            return False


# determines whether a task is within a certain time constraint
def date_control(req, user_object, req_range):
    if req == "":
        return True
    else:
        if "on" in req_range:
            if str(user_object.Date_Worked) == req:
                return True
        if "before" in req_range:
            object_date = datetime.date(int(str(user_object.Date_Worked).split("-")[0]),
                                        int(str(user_object.Date_Worked).split("-")[1]),
                                        int(str(user_object.Date_Worked).split("-")[2]))
            req_date = datetime.date(int(req.split("-")[0]), int(req.split("-")[1]), int(req.split("-")[2]))
            if object_date < req_date:
                return True
        if "after" in req_range:
            object_date = datetime.date(int(str(user_object.Date_Worked).split("-")[0]),
                                        int(str(user_object.Date_Worked).split("-")[1]),
                                        int(str(user_object.Date_Worked).split("-")[2]))
            req_date = datetime.date(int(req.split("-")[0]), int(req.split("-")[1]), int(req.split("-")[2]))
            if object_date > req_date:
                return True
        else:
            return False
