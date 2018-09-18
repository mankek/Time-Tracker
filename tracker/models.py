from django.db import models


class Code(models.Model):

    def __str__(self):
        return str(self.code_text)

    code_text = models.CharField(max_length=200)


class Task(models.Model):

    def __str__(self):
        return str(self.task_code)

    performed_by = models.ForeignKey('login.User', on_delete=models.CASCADE)
    task_code = models.ForeignKey(Code, on_delete=models.CASCADE)


class Time(models.Model):

    def __str__(self):
        return str(self.time_hours) + " hours and " + str(self.time_minutes) + " minutes"

    time_hours = models.SmallIntegerField(default=0)
    time_minutes = models.IntegerField(default=0)
    date_performed = models.DateField(auto_now=True)
    task_performed = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)



