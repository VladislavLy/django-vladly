import random

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from faker import Faker

from .forms import StudentForm
from .models import Student


def index(request):
    return render(request, 'students/wrapper.html')


def generate_student(request):
    fake = Faker()
    Student.objects.all().delete()

    student = Student.objects.create(
        name=fake.first_name(),
        surname=fake.last_name(),
        age=random.randint(10, 50), )

    return render(request, 'students/students.html', {"Title": 'Student', "object": student})


def generate_students(request):
    faker = Faker()
    Student.objects.all().delete()

    if request.method == 'GET':
        count = request.GET.get('count', '5')
        try:
            count = int(count)
        except Exception:
            return HttpResponse(f'<h3>{count} is not an integer!</h3>')

        if count <= 100 and count > 0:
            for i in range(int(count)):
                Student.objects.create(
                    name=faker.first_name(),
                    surname=faker.last_name(),
                    age=faker.random.randint(10, 50),)

            student_list = Student.objects.all()

            return render(request, 'students/students.html', {"Title": 'Students', "object_list": student_list})

    return HttpResponse('<h3>Something went wrong... Try it in another way!</h3>')


def generate_students_count(request, number):
    fake = Faker()
    result = []
    Student.objects.all().delete()
    try:
        number = int(number)
    except Exception:
        return HttpResponse(f'<h3>{number} is not an integer!</h3>')

    if number <= 100 and number > 0:
        for i in range(number):
            result.append(Student(
                name=fake.first_name(),
                surname=fake.last_name(),
                age=fake.random.randint(15, 35),))

    Student.objects.bulk_create(result)
    output = Student.objects.all()

    return render(request, 'students/students.html', {"Title": 'Students', "object_list": output})


def list_of_students(request):
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

            students_list = Student.objects.all().filter(**output_dict)
            return render(request, 'students/students.html', {"Title": 'Students', "object_list": students_list})

    students_list = Student.objects.all().order_by('-id')
    return render(request, 'students/students.html', {"Title": 'Students', "object_list": students_list})


def create_student(request):
    error = ''
    if request.method == 'POST' and not request.POST.get('error'):
        our_form = StudentForm(request.POST)
        if our_form.is_valid():
            our_form.save()
            return redirect('list_of_students')
        else:
            error = "Form isn't valid!"
    elif request.method == 'POST' and request.POST.get('error'):
        our_form = StudentForm(request.POST)
        context = {
            'form': our_form,
            'error': error,
            'Title': 'Student',
        }
    else:
        our_form = StudentForm()
        context = {
            'form': our_form,
            'error': error,
            'Title': 'Student',
        }

    return render(request, 'students/create_student.html', context)


def edit_student(request, student_id):
    if request.method == 'POST' and not request.POST.get('error'):
        form = StudentForm(request.POST)
        if form.is_valid():
            Student.objects.update_or_create(id=student_id, defaults=form.cleaned_data)
            return redirect('list_of_students')
    else:
        student = Student.objects.filter(id=student_id).first()
        form = StudentForm(instance=student)

    return render(request, 'students/edit_student.html', {"form": form, 'student_id': student_id, 'Title': 'Student'})


def delete_student(request, student_id):
    student = Student.objects.filter(id=student_id)
    student.delete()
    return redirect('list_of_students')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'students/wrapper.html')


class GenerateStudent(View):
    def get(self, request, *args, **kwargs):
        fake = Faker()
        Student.objects.all().delete()

        student = Student.objects.create(
            name=fake.first_name(),
            surname=fake.last_name(),
            age=random.randint(10, 50),
            phone=fake.msisdn(),)

        return render(request, 'students/students.html', {"Title": 'Student', "object": student})


class GenerateStudents(View):
    def get(self, request, *args, **kwargs):
        faker = Faker()
        Student.objects.all().delete()

        count = request.GET.get('count', '5')
        try:
            count = int(count)
        except Exception:
            return HttpResponse(f'<h3>{count} is not an integer!</h3>')

        if count <= 100 and count > 0:
            for i in range(int(count)):
                Student.objects.create(
                    name=faker.first_name(),
                    surname=faker.last_name(),
                    age=faker.random.randint(10, 50),
                    phone=faker.msisdn(),)

            student_list = Student.objects.all()

            return render(request, 'students/students.html', {"Title": 'Students', "object_list": student_list})
        return HttpResponse('<h3>Something went wrong... Try it in another way!</h3>')


class GenerateStudentsCount(View):
    def get(self, request, *args, **kwargs):
        fake = Faker()
        result = []
        Student.objects.all().delete()
        try:
            number = int(kwargs['number'])
        except Exception:
            a = kwargs['number']
            return HttpResponse(f'<h3>{a} is not an integer!</h3>')

        if number <= 100 and number > 0:
            for i in range(number):
                result.append(Student(
                    name=fake.first_name(),
                    surname=fake.last_name(),
                    age=fake.random.randint(15, 35),
                    phone=fake.msisdn(),))

            Student.objects.bulk_create(result)
            output = Student.objects.all()
            return render(request, 'students/students.html', {"Title": 'Students', "object_list": output})
        return HttpResponse('<h3>Something went wrong... Try it in another way!</h3>')


class ListOfStudents(ListView):
    paginate_by = 5
    model = Student
    template_name = 'students/students.html'
    context_object_name = 'object_list'
    allow_empty = False

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Students'
        return data

    def get_queryset(self):
        queryset = Student.objects.all().order_by('-id')

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
        return queryset


class CreateStudent(CreateView):
    model = Student
    template_name = 'students/create_student.html'
    form_class = StudentForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Student'
        return data

    def form_valid(self, form):
        Student.objects.create(**form.cleaned_data)
        return redirect('list_of_students')

    def post(self, request, *args, **kwargs):
        post = self.request.POST.copy()
        self.request.POST = post
        if not request.POST.get('phone').strip().isdigit() and bool(request.POST.get('phone')):
            from django.contrib import messages
            request.POST.__setitem__('error', 666)
            messages.error(request, f"ERROR! {request.POST.get('phone')} -It's not a digit! Try again!") # noqa

        if not self.request.POST.get('error'):
            our_form = StudentForm(self.request.POST)
            if our_form.is_valid():
                our_form.save()
                return redirect('list_of_students')
        elif self.request.POST.get('error'):
            our_form = StudentForm(self.request.POST)
        else:
            our_form = StudentForm()
        return render(request, 'students/create_student.html', {'Title': 'Student', 'form': our_form})


class EditStudent(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/edit_student.html'
    success_url = reverse_lazy('list_of_students')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Student'
        return data

    def post(self, request, *args, **kwargs):
        post = self.request.POST.copy()
        self.request.POST = post
        the_object = self.get_object()
        if not request.POST.get('phone').strip().isdigit() and bool(request.POST.get('phone')):
            from django.contrib import messages
            request.POST.__setitem__('error', 666)
            messages.error(request, f"ERROR! {request.POST.get('phone')} -It's not a digit! Try again!") # noqa

        if not self.request.POST.get('error'):
            our_form = StudentForm(self.request.POST)
            if our_form.is_valid():
                Student.objects.update_or_create(id=the_object.__dict__['id'], defaults=our_form.cleaned_data)
                return redirect('list_of_students')
        elif self.request.POST.get('error'):
            our_form = StudentForm(self.request.POST)
        else:
            our_form = StudentForm()
        return render(request, 'students/edit_student.html', {'Title': 'Student', 'form': our_form, 'object': the_object})


class DeleteStudent(DeleteView):
    model = Student
    success_url = reverse_lazy('list_of_students')
    template_name = 'students/students.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


def handler404(request, exception):
    return render(request, 'students/errors/404page.html', status=404)


def handler500(request):
    return render(request, 'students/errors/500page.html', status=500)
