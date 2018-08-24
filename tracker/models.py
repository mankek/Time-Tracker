from django.db import models


# Create your models here.
class Username(models.Model):

    def __str__(self):
        return self.username_text

    username_text = models.CharField(max_length=100)
    department = models.CharField(max_length=100)


class Task(models.Model):

    def __str__(self):
        return self.task_text

    performed_by = models.ForeignKey(Username, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)


class Time(models.Model):

    def __str__(self):
        return str(self.time_hours) + " hours and " + str(self.time_minutes) + " minutes"

    time_hours = models.SmallIntegerField(default=0)
    time_minutes = models.IntegerField(default=0)
    date_performed = models.DateField(auto_now=True)
    task_performed = models.ForeignKey(Task, on_delete=models.CASCADE)
