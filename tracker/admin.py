from django.contrib import admin
from .models import WorkCode, WorkHour

# Register your models here.


admin.site.register(WorkHour)
admin.site.register(WorkCode)
