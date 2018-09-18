from django.contrib import admin
from .models import Task, Time, Code

# Register your models here.


class TimeAdmin(admin.ModelAdmin):
    list_display = ('date_performed', 'task_text', 'task_performed', 'time_hours', 'time_minutes')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_code', 'performed_by')


admin.site.register(Time, TimeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Code)
