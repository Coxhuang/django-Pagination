from django.db import models



class Student(models.Model):

    name = models.CharField(max_length=128)
    age = models.CharField(max_length=128)