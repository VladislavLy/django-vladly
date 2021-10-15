from django.core.management import call_command

from groups.models import Group

import pytest

from students.models import Student

from ..models import Teacher


@pytest.mark.django_db
def test_call_cammand():
    args = ['1']
    opts = {}
    call_command('generate_teachers', *args, **opts)
    assert Teacher.objects.count() == 1
    assert Group.objects.count() == 1
    assert 1 <= Student.objects.count() <= 9
