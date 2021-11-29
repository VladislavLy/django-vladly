from django.forms.models import model_to_dict
from django.test import Client

import pytest

from pytest_django.asserts import assertTemplateUsed

from .. forms import GroupForm
from ..models import Group


@pytest.mark.django_db
def test_generate_groups():
    x = Client().get('/groups-generate/')
    assert Group.objects.count() == 10
    assert x.status_code == 200


@pytest.mark.django_db
def test_list_of_groups(admin_client):
    x = admin_client.post("/create-group/", data={'subject': 'Music', 'ratio_of_students': 2})
    assert x.status_code == 302
    response = admin_client.get('/list-of-groups/')
    assert response.status_code == 200
    assert Group.objects.count() == 1
    assertTemplateUsed(response, 'groups/groups.html')


@pytest.mark.django_db
def test_create_group(admin_client):
    x = admin_client.post("/create-group/", data={'subject': 'Music', 'ratio_of_students': 2})
    assert x.status_code == 302
    assert Group.objects.count() == 1
    response = admin_client.get('/create-group/')
    assertTemplateUsed(response, 'groups/create_group.html')


@pytest.mark.django_db
def test_delete_group(admin_client):
    x = admin_client.post("/create-group/", data={'id': 1, 'subject': 'Music', 'ratio_of_students': 2})
    assert Group.objects.count() == 1
    group = Group.objects.last()
    group.delete()
    assert Group.objects.count() == 0
    assert x.status_code == 302


@pytest.mark.django_db
def test_post_edit_group(admin_client):
    y = admin_client.post("/create-group/", data={'id': 1, 'subject': 'Music', 'ratio_of_students': 2})
    x = admin_client.post("/edit-group/1/", data={'id': 1, 'subject': 'Music', 'ratio_of_students': 2})
    assert model_to_dict(Group.objects.get(id=1)) == {'id': 1, 'subject': 'Music', 'ratio_of_students': 2, 'main_teacher': None}
    assert 'Music' in Group.objects.last().__str__()
    assert x.status_code == 302
    assert y.status_code == 302
    response = admin_client.get('/edit-group/1/')
    assertTemplateUsed(response, 'groups/edit_group.html')


@pytest.mark.django_db
def test_group_form():
    form = GroupForm(data={'subject': 'Music', 'ratio_of_students': 2})
    assert form.is_valid()


@pytest.mark.django_db
def test_capitalize_group(admin_client):
    c = admin_client
    x = c.post("/create-group/", data={'subject': 'music', 'ratio_of_students': 2})
    assert Group.objects.get(id=1).subject == "Music"
    assert x.status_code == 302


@pytest.mark.django_db
def test_list_of_groups_querry(admin_client):
    x = admin_client.post("/create-group/", data={'subject': 'Music', 'ratio_of_students': 2})
    assert x.status_code == 302
    response = admin_client.get('/list-of-groups/?subject=Music')
    assert response.status_code == 200
    assert Group.objects.count() == 1
