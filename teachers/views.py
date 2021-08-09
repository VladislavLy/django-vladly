from django.shortcuts import render
from .models import Teacher
from faker import Faker
from random import randrange
import random


def generate_teachers(request, number=10):
    fake = Faker()
    result=[]
    Teacher.objects.all().delete()

    for i in range(number):
        result.append(Teacher(
            name= fake.first_name(), 
            surname= fake.last_name(), 
            age= fake.random.randint(20,60),))

    Teacher.objects.bulk_create(result)
    output = Teacher.objects.all()
    
    return render(request, 'teachers/teachers.html', {"Title":'Teachers', "object_list": output})

