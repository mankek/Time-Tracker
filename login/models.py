from django.db import models

# Create your models here.


class User(models.Model):
    def __str__(self):
        return self.username_text

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username_text = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
