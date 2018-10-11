from django.db import models


class WorkCode(models.Model):

    def __str__(self):
        return str(self.Description)

    Description = models.CharField(max_length=200)
    Billable = models.BooleanField()


class WorkHour(models.Model):

    def __str__(self):
        return str(self.Employee) + ": " + str(self.Work_Code)

    Employee = models.ForeignKey('login.Employee', on_delete=models.CASCADE)
    Date_Worked = models.DateField()
    Work_Code = models.ForeignKey(WorkCode, on_delete=models.CASCADE)
    Hours = models.SmallIntegerField(default=0)
    Minutes = models.IntegerField(default=0)
    Work_Description = models.CharField(max_length=200)




