from django.shortcuts import HttpResponse, render

from faker import Faker

from .models import Teacher

import random # noqa


def generate_teachers(request, number=10):
    fake = Faker()
    result = []
    Teacher.objects.all().delete()

    for i in range(number):
        result.append(Teacher(
            name=fake.first_name(),
            surname=fake.last_name(),
            age=fake.random.randint(19, 70),))

    Teacher.objects.bulk_create(result)
    output = Teacher.objects.all()

    return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": output})


def list_of_teachers(request):
    if request.method == 'GET':
        if request.GET.get('age', '') or request.GET.get('name', '') or request.GET.get('surname', ''):
            parameter_age = request.GET.get('age', None)
            parameter_name = request.GET.get('name', None)
            parameter_surname = request.GET.get('surname', None)

            try:
                if parameter_age is None:
                    pass
                else:
                    parameter_age = int(parameter_age)
            except Exception:
                return HttpResponse(f'<h3>{parameter_age} is not an integer!</h3>')

            param_dict = {'age': parameter_age, 'name': parameter_name, 'surname': parameter_surname}
            output_dict = {}

            for key, value in param_dict.items():
                if value is not None:
                    output_dict.update({key: value})

            teachers_list = Teacher.objects.all().filter(**output_dict)
            return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": teachers_list})

    teachers_list = Teacher.objects.all().order_by('name')
    return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": teachers_list})


def list_of_teachers_param(request, **kwargs):
    teachers_list = Teacher.objects.all().filter(**kwargs)
    return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": teachers_list})
