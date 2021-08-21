from random import randrange

from django.http import HttpResponse
from django.shortcuts import redirect, render

from faker import Faker

from .forms import GroupForm
from .models import Group


def groups_db(request, group_number=10):
    faker = Faker()
    result = []
    Group.objects.all().delete()

    for i in range(group_number):
        result.append(
            Group(
                subject=faker.job(),
                ratio_of_students=randrange(5, 20),
            )
        )
    Group.objects.bulk_create(result)
    output = Group.objects.all()

    return render(request, 'groups/groups.html', {"Title": 'Groups', "object_list": output})


def list_of_groups(request):
    if request.method == 'GET':
        if request.GET.get('subject', '') or request.GET.get('ratio_of_students', ''):
            ratio_of_students = request.GET.get('ratio_of_students', None)
            subject = request.GET.get('subject', None)

            try:
                if ratio_of_students is None:
                    pass
                else:
                    ratio_of_students = int(ratio_of_students)
            except Exception:
                return HttpResponse(f'<h3>{ratio_of_students} is not an integer!</h3>')

            param_dict = {'ratio_of_students': ratio_of_students, 'subject': subject, }
            output_dict = {}

            for key, value in param_dict.items():
                if value is not None:
                    output_dict.update({key: value})

            groups_list = Group.objects.all().filter(**output_dict)
            return render(request, 'groups/groups.html', {"Title": 'Groups', "object_list": groups_list})

    groups_list = Group.objects.all().order_by('-id')
    return render(request, 'groups/groups.html', {"Title": 'Groups', "object_list": groups_list})


def create_group(request):
    if request.method == 'GET':
        our_form = GroupForm()

    elif request.method == 'POST':
        our_form = GroupForm(request.POST)
        if our_form.is_valid():
            Group.objects.create(**our_form.cleaned_data)
            return redirect('list_of_groups')

    return render(request, 'groups/create_group.html', {"Title": 'Group', "form": our_form})
