from django.contrib import admin
from .models import Task, Time, Code

# Register your models here.


admin.site.register(Time)
admin.site.register(Task)
admin.site.register(Code)
