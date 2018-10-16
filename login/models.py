from django.db import models

# Create your models here.


class Employee(models.Model):
    def __str__(self):
        return str(self.Username)

    Last_Name = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Username = models.CharField(max_length=50)
    Email_Address = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)
    Team = models.CharField(max_length=100)
    Active = models.BooleanField()
