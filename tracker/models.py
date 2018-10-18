from django.db import models


class Cat(models.Model):

    def __str__(self):
        return str(self.Category)

    Category = models.CharField(max_length=50)


class SubCat(models.Model):

    def __str__(self):
        return str(self.Parent_Category) + "-" + str(self.SubCategory)

    SubCategory = models.CharField(max_length=50)
    Parent_Category = models.ForeignKey(Cat, on_delete=models.CASCADE)


class WorkHour(models.Model):

    def __str__(self):
        return str(self.Employee) + ": " + str(self.Task_Category)

    Employee = models.ForeignKey('login.Employee', on_delete=models.CASCADE)
    Date_Worked = models.DateField()
    Task_Category = models.ForeignKey(SubCat, on_delete=models.CASCADE)
    Hours = models.SmallIntegerField(default=0)
    Minutes = models.IntegerField(default=0)
    Work_Description = models.CharField(max_length=200)
    Rework = models.BooleanField()




