from django.contrib import admin
from .models import Username, Task, Time

# Register your models here.
admin.site.register(Username)
admin.site.register(Task)
admin.site.register(Time)
