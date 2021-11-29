from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render

from faker import Faker

from .models import Teacher

import random # noqa

from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import TeacherForm


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

    teachers_list = Teacher.objects.all().order_by('-id')
    return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": teachers_list})


def list_of_teachers_param(request, **kwargs):
    teachers_list = Teacher.objects.all().filter(**kwargs)
    return render(request, 'teachers/teachers.html', {"Title": 'Teachers', "object_list": teachers_list})


def create_teacher(request):
    error = ''

    if request.method == 'GET':
        our_form = TeacherForm()
        context = {
            'form': our_form,
            'error': error,
            'Title': 'Teacher',
        }

    elif request.method == 'POST':
        our_form = TeacherForm(request.POST)
        if our_form.is_valid():
            our_form.save()
            return redirect('list_of_teachers')
        else:
            error = "Form isn't valid!"

    return render(request, 'teachers/create_teacher.html', context)


def edit_teacher(request, teacher_id):
    if request.method == 'GET':
        teacher = Teacher.objects.filter(id=teacher_id).first()
        form = TeacherForm(instance=teacher)

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            Teacher.objects.update_or_create(id=teacher_id, defaults=form.cleaned_data)
            return redirect('list_of_teachers')

    return render(request, 'teachers/edit_teacher.html', {"form": form, 'teacher_id': teacher_id, 'Title': 'Teacher'})


def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.filter(id=teacher_id)
    teacher.delete()
    return redirect('list_of_teachers')


class GenerateTeachers(View):
    def get(self, request, *args, **kwargs):
        fake = Faker()
        result = []
        Teacher.objects.all().delete()
        number = 10
        for _ in range(number):
            result.append(Teacher(
                name=fake.first_name(),
                surname=fake.last_name(),
                age=fake.random.randint(19, 70),
                ))

        Teacher.objects.bulk_create(result)
        output = Teacher.objects.all()
        return render(request, 'teachers/teachers.html', {"Title": 'Students', "object_list": output})


class ListOfTeachers(ListView):
    paginate_by = 5
    model = Teacher
    template_name = 'teachers/teachers.html'
    context_object_name = 'object_list'
    allow_empty = False

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Teachers'
        return data

    def get_queryset(self):
        queryset = Teacher.objects.all().order_by('-id')

        if self.request.GET.get('name', '') or self.request.GET.get('age', '') or self.request.GET.get('surname', ''):
            parameter_age = self.request.GET.get('age', None)
            parameter_name = self.request.GET.get('name', None)
            parameter_surname = self.request.GET.get('surname', None)
            try:
                if parameter_age is None:
                    pass
                else:
                    parameter_age = int(parameter_age)
            except Exception:
                return queryset

            param_dict = {'age': parameter_age, 'name': parameter_name, 'surname': parameter_surname}
            output_dict = {}

            for key, value in param_dict.items():
                if value is not None:
                    output_dict.update({key: value})
            queryset = queryset.filter(**output_dict)
        elif self.kwargs:
            queryset = Teacher.objects.all().filter(**self.kwargs)
        return queryset


class CreateTeacher(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Teacher
    template_name = 'teachers/create_teacher.html'
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Teacher'
        return data

    def form_valid(self, form):
        Teacher.objects.create(**form.cleaned_data)
        return redirect('list_of_teachers')


class EditTeacher(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/edit_teacher.html'
    success_url = reverse_lazy('list_of_teachers')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Teacher'
        return data

    def post(self, request, *args, **kwargs):
        the_object = self.get_object()
        our_form = TeacherForm(self.request.POST)
        if our_form.is_valid():
            Teacher.objects.update_or_create(id=the_object.__dict__['id'], defaults=our_form.cleaned_data)
            return redirect('list_of_teachers')


class DeleteTeacher(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Teacher
    success_url = reverse_lazy('list_of_teachers')
    template_name = 'teachers/teachers.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
