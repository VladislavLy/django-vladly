from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.test import Client

import pytest

from pytest_django.asserts import assertTemplateUsed

from pytz import timezone

from .. forms import StudentForm
from ..models import Logger, Student
from ..tasks import delete_logs


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('Johny', 'abc@mail.com', 'passwordabc')
    assert User.objects.count() == 1


@pytest.mark.urls('mysite.urls')
def test_main(client):
    response = client.get('')
    assert response.status_code == 200
    assert 'Home' in response.content.decode()
    assertTemplateUsed(response, 'students/wrapper.html')


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_error_404():
    c = Client()
    response = c.get("/stu404dents/")
    assert response.status_code == 404
    assertTemplateUsed(response, 'students/errors/404page.html')


@pytest.mark.django_db
def test_generate_student():
    x = Client().get('/generate-student/')
    assert Student.objects.count() == 1
    assert x.status_code == 200


@pytest.mark.django_db
def test_generate_students():
    x = Client().get('/generate-students/?count=6')
    assert Student.objects.count() == 6
    assert x.status_code == 200


@pytest.mark.django_db
def test_generate_students_count():
    x = Client().get('/generate-students-count/10')
    assert Student.objects.count() == 10
    assert x.status_code == 200


@pytest.mark.django_db
def test_list_of_students():
    x = Client().post("/create-student/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '29',
                                                'phone': 380991010101,
                                                })
    assert x.status_code == 302
    response = Client().get('/list-of-students/')
    assert response.status_code == 200
    assert Student.objects.count() == 1
    assertTemplateUsed(response, 'students/students.html')
    assert '<h1 class="tab">Students</h1>' in response.content.decode()


@pytest.mark.django_db
def test_create_student():
    x = Client().post("/create-student/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '29',
                                                'phone': 380991010101,
                                                })
    assert x.status_code == 302
    assert Student.objects.count() == 1
    assert Student.objects.get(pk=1).name == 'Johny'
    assert Student.objects.get(pk=1).surname == 'D'
    response = Client().get('/create-student/')
    assertTemplateUsed(response, 'students/create_student.html')


@pytest.mark.django_db
def test_delete_student():
    x = Client().post("/create-student/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'D',
                                                'age': '29',
                                                'phone': 380991010101,
                                                })
    assert Student.objects.count() == 1
    student = Student.objects.last()
    student.delete()
    assert Student.objects.count() == 0
    assert x.status_code == 302


@pytest.mark.django_db
def test_post_edit_student():
    Client().get("/generate-student/")
    assert Student.objects.count() == 1

    x = Client().post("/edit-student/1/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'D',
                                                'age': '29',
                                                'phone': 380991010101,
                                                })
    assert model_to_dict(Student.objects.get(id=1)) == {'id': 1,
                                                        'name': 'Johny',
                                                        'surname': 'D',
                                                        'age': 29,
                                                        'phone': '380991010101',
                                                        'in_the_group': None,
                                                        }
    assert 'Johny' in Student.objects.last().__str__()
    assert x.status_code == 302
    response = Client().get('/edit-student/1/')
    assertTemplateUsed(response, 'students/edit_student.html')


@pytest.mark.django_db
def test_phone():
    x = Client().post("/create-student/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'D',
                                                'age': '29',
                                                'phone': '+380(99)1010101aaa'
                                                })
    a = Student.objects.last()
    assert a is None
    assert x.status_code == 200
    response = Client().get('/create-student/')
    assertTemplateUsed(response, 'students/create_student.html')


@pytest.mark.django_db
def test_capitalize_student():
    c = Client()
    x = c.post("/create-student/", data={'name': 'johny',
                                         'surname': 'd',
                                         'age': '29',
                                         'phone': 380991010101,
                                         })
    assert Student.objects.get(id=1).name == "Johny"
    assert Student.objects.get(id=1).surname == "D"
    assert x.status_code == 302
    response = Client().get('/create-student/')
    assertTemplateUsed(response, 'students/create_student.html')


@pytest.mark.django_db
def test_logger():
    Client().get("/admin/")
    delete_logs()
    instance = Logger.objects.filter(created__lte=datetime.now(timezone('UTC')) - timedelta(days=7))
    assert instance.count() == 0
    assert '' in instance.last().__str__()


@pytest.mark.django_db
def test_students_form():
    form = StudentForm(data={'name': 'Johny',
                             'surname': 'D',
                             'age': 29,
                             'phone': 380991010101,
                             })
    assert form.is_valid()


@pytest.mark.django_db
def test_list_of_students_querry():
    x = Client().post("/create-student/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '31',
                                                'phone': 380991010101,
                                                })
    assert x.status_code == 302
    response_1 = Client().get('/list-of-students/?age=31')
    response_2 = Client().get('/list-of-students/?name=Johny')
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert Student.objects.count() == 1
    response = Client().get('/list-of-students/')
    assertTemplateUsed(response, 'students/students.html')
