from django.forms.models import model_to_dict
from django.test import Client

import pytest

from pytest_django.asserts import assertTemplateUsed

from .. forms import TeacherForm
from ..models import Teacher


@pytest.mark.django_db
def test_generate_teachers():
    x = Client().get('/generate-teachers/')
    assert Teacher.objects.count() == 10
    assert x.status_code == 200


@pytest.mark.django_db
def test_list_of_teachers():
    x = Client().post("/create-teacher/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '50',
                                                })
    assert x.status_code == 302
    response = Client().get('/list-of-teachers/')
    assert response.status_code == 200
    assert Teacher.objects.count() == 1
    assertTemplateUsed(response, 'teachers/teachers.html')


@pytest.mark.django_db
def test_create_teacher():
    x = Client().post("/create-teacher/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '50',
                                                })
    assert x.status_code == 302
    assert Teacher.objects.count() == 1
    assert Teacher.objects.get(pk=1).name == 'Johny'
    assert Teacher.objects.get(pk=1).surname == 'D'
    response = Client().get('/create-teacher/')
    assertTemplateUsed(response, 'teachers/create_teacher.html')


@pytest.mark.django_db
def test_delete_teacher():
    x = Client().post("/create-teacher/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'D',
                                                'age': '50',
                                                })
    assert Teacher.objects.count() == 1
    teacher = Teacher.objects.last()
    teacher.delete()
    assert Teacher.objects.count() == 0
    assert x.status_code == 302


@pytest.mark.django_db
def test_post_edit_teacher():
    y = Client().post("/create-teacher/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'D',
                                                'age': '50',
                                                })
    x = Client().post("/edit-teacher/1/", data={'id': 1,
                                                'name': 'Johny',
                                                'surname': 'Ddd',
                                                'age': '50',
                                                })
    assert model_to_dict(Teacher.objects.get(id=1)) == {'id': 1,
                                                        'name': 'Johny',
                                                        'surname': 'Ddd',
                                                        'age': 50,
                                                        'subject_class': '',
                                                        }
    assert 'Johny' and 'Ddd' in Teacher.objects.last().__str__()
    assert x.status_code == 302
    assert y.status_code == 302
    response = Client().get('/edit-teacher/1/')
    assertTemplateUsed(response, 'teachers/edit_teacher.html')


@pytest.mark.django_db
def test_teacher_form():
    form = TeacherForm(data={'name': 'Johny',
                             'surname': 'D',
                             'age': 50,
                             })
    assert form.is_valid()


@pytest.mark.django_db
def test_list_of_teachers_querry():
    x = Client().post("/create-teacher/", data={'name': 'Johny',
                                                'surname': 'D',
                                                'age': '40',
                                                })
    assert x.status_code == 302
    response_1 = Client().get('/list-of-teachers/?age=40')
    response_2 = Client().get('/list-of-teachers/?name=Johny')
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert Teacher.objects.count() == 1


@pytest.mark.django_db
def test_capitalize_teacher():
    c = Client()
    x = c.post("/create-teacher/", data={'name': 'johny',
                                         'surname': 'd',
                                         'age': '50',
                                         })
    assert Teacher.objects.get(id=1).name == "Johny"
    assert Teacher.objects.get(id=1).surname == "D"
    assert x.status_code == 302
