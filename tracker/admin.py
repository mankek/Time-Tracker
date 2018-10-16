from django.contrib import admin
from .models import Cat, SubCat, WorkHour

# Register your models here.


admin.site.register(WorkHour)
admin.site.register(Cat)
admin.site.register(SubCat)
