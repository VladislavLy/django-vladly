from django.core.mail import send_mail
from django.test import Client, override_settings # noqa

import pytest

from pytest_django.asserts import assertTemplateUsed

from ..forms import ContactForm
from ..tasks import send_email_contact # noqa


def test_email():
    assert send_mail("test title",
                     "test message",
                     "example@mail.com",
                     ["hahaexample@gmail.com"],
                     )
    response = Client().get('/contact-us/')
    assertTemplateUsed(response, 'contact/contact_form.html')
    assert response.status_code == 200


def test_get_contact():
    c = Client()
    x = c.get("/contact-us/")
    assert x.status_code == 200
    assertTemplateUsed(x, 'contact/contact_form.html')


@pytest.mark.django_db
def test_contact_us_form():
    form = ContactForm(data={'title': 'Example title',
                             'message': 'Example message',
                             'email_from': 'example@mail.com',
                             })
    assert form.is_valid()
    response = Client().get('/contact-us/')
    assertTemplateUsed(response, 'contact/contact_form.html')
    assert response.status_code == 200
    assert '<h1 align="center"> Contact us </h1>' in response.content.decode()


def test_empty_form():
    form = ContactForm(data={})
    assert not form.is_valid()
    response = Client().get('/contact-us/')
    assertTemplateUsed(response, 'contact/contact_form.html')


@override_settings(CELERY_ALWAYS_EAGER=True)
def test_celery_email(client):
    test_data = {'title': 'example title',
                 'message': 'example message',
                 'email_from': 'example@gmail.com'}
    response = client.post('/contact-us/', data=test_data)
    assert response.status_code == 302
    the_task = send_email_contact(title=test_data.get('title'),
                                  email_from=test_data.get('message'),
                                  message=test_data.get('email_from'),
                                  )
    # assert the_task == "Success"
    assert bool(the_task)
