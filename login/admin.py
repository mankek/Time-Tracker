from django.contrib import admin
from .models import Employee
import os


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['First_Name', 'Last_Name', 'Team']
    ordering = ['First_Name']
    actions = ['download_data']

    def get_fields(self, request, obj=None):
        fields = super(EmployeeAdmin, self).get_fields(request, obj)
        if obj:
            fields.remove('Password')
        return fields

    def download_data(self, request, queryset):
        path = os.path.abspath(__file__).split("\\")[0:3]
        path.append('Desktop\\')
        if os.path.exists("\\".join(path)):
            with open(r"C:\Users\krmanke\Desktop\Employee Time Records.csv", mode='w') as file_out:
                file_out.write("First Name, Last Name, Category, Subcategory, Date, Hours, Minutes, Description, Rework\n")
                for i in queryset:
                    for s in i.workhour_set.all():
                        file_out.write(str(i.First_Name) + "," + str(i.Last_Name) + ",")
                        file_out.write(str(s.Task_Category).split("-")[0] + "," + str(s.Task_Category).split("-")[1] + ",")
                        file_out.write(str(s.Date_Worked) + "," + str(s.Hours) + "," + str(s.Minutes) + ",")
                        file_out.write(str(s.Work_Description) + "," + str(s.Rework) + "\n")
            file_out.close()
            self.message_user(request, "The file Employee Time Records.csv was successfully created on your Desktop.")
        else:
            self.message_user(request, "Desktop not found.")
    download_data.short_description = "Download data"


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
