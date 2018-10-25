from django.contrib import admin
from .models import Employee


def download_data(modeladmin, request, queryset):
    with open("Employee Time Records.csv", mode='w') as file_out:
        file_out.write("First Name, Last Name, Category, Subcategory, Date, Hours, Minutes, Description, Rework\n")
        for i in queryset:
            for s in i.workhour_set.all():
                file_out.write(str(i.First_Name) + "," + str(i.Last_Name) + ",")
                file_out.write(str(s.Task_Category).split("-")[0] + "," + str(s.Task_Category).split("-")[1] + ",")
                file_out.write(str(s.Date_Worked) + "," + str(s.Hours) + "," + str(s.Minutes) + ",")
                file_out.write(str(s.Work_Description) + "," + str(s.Rework) + "\n")
    file_out.close()
    download_data.short_description = "Test for download"


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['First_Name', 'Last_Name', 'Team']
    ordering = ['First_Name']
    actions = [download_data]


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
