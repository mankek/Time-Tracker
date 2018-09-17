from django.contrib import admin
from .models import Task, Time

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_code', 'performed_by')


class TimeAdmin(admin.ModelAdmin):
    list_display = ('date_performed', 'time_hours', 'time_minutes', 'task_performed')


admin.site.register(Time, TimeAdmin)
admin.site.register(Task, TaskAdmin)