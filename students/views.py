from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from faker import Faker
from random import randrange
import random


def index(request):
    return render(request, 'students/wrapper.html')


def generate_student(request):
    fake = Faker()
    Student.objects.all().delete()

    student = Student.objects.create(
        name = fake.first_name(), 
        surname = fake.last_name(), 
        age = random.randint(10,50),)

    return render(request, 'students/students.html', {"Title":'Student', "object": student})
    

def generate_students(request):
    faker = Faker()
    Student.objects.all().delete()

    if request.method == 'GET':
	    count = request.GET.get('count', '5')
	    try:
		    count = int(count)
	    except:
		    return HttpResponse(f'<h3>{count} is not an integer!</h3>')
        
	    if count <= 100 and count > 0:
		    for i in range(int(count)):
			    student = Student.objects.create(
                name= faker.first_name(), 
                surname= faker.last_name(), 
                age= faker.random.randint(10,50),)
                
		    student_list = Student.objects.all()
    
		    return render(request, 'students/students.html', {"Title":'Students', "object_list": student_list})

    return	HttpResponse('<h3>Something went wrong... Try it in another way!</h3>')


def generate_students_count(request, number):
    fake = Faker()
    result=[]
    Student.objects.all().delete()
    try:
        number= int(number)
    except:
        return HttpResponse(f'<h3>{number} is not an integer!</h3>')

    if number <= 100 and number > 0:
        for i in range(number):
            result.append(Student(
                name= fake.first_name(), 
                surname= fake.last_name(), 
                age= fake.random.randint(15,35),))

    Student.objects.bulk_create(result)
    output = Student.objects.all()
    
    return render(request, 'students/students.html', {"Title":'Students', "object_list": output})




