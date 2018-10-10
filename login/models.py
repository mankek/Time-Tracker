from django.db import models

# Create your models here.


class Employee(models.Model):
    def __str__(self):
        return str(self.First_Name) + " " + str(self.Last_Name)

    Company = models.CharField(max_length=250)
    Last_Name = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Username = models.CharField(max_length=50)
    Email_Address = models.EmailField(max_length=100)
    Job_Title = models.CharField(max_length=100)
    Business_Phone = models.CharField(max_length=25, default="None")
    Home_Phone = models.CharField(max_length=25, default="None")
    Mobile_Phone = models.CharField(max_length=25, default="None")
    Fax_Number = models.CharField(max_length=25, default="None")
    Address = models.CharField(max_length=250)
    City = models.CharField(max_length=100)
    State_Province = models.CharField(max_length=100)
    ZIP = models.PositiveIntegerField()
    Country_Region = models.CharField(max_length=100, default="United States of America")
    Web_Page = models.URLField(max_length=100)
    Notes = models.TextField(default="None")
