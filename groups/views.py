from django.shortcuts import render
from faker import Faker
from random import randrange
from .models import Group


def groups_db(request, group_number = 10):
    faker = Faker()
    result = []
    Group.objects.all().delete()

    for i in range(group_number):
        result.append(
            Group(
                subject = faker.job(),
                ratio_of_students = randrange(5, 20),
            )
        )
    Group.objects.bulk_create(result)
    output = Group.objects.all()

    return render(request, 'groups/groups.html', {"Title":'Groups', "object_list": output})
