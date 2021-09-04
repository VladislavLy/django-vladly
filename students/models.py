from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    phone = models.CharField(null=True, blank=True, max_length=15)

    def __str__(self):
        return f'{self.name} {self.surname} {self.age} {self.phone}'


class Logger(models.Model):
    method = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    execution_time = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
