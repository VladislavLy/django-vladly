from django.core.mail import send_mail
from django.test import Client

import pytest

from pytest_django.asserts import assertTemplateUsed

from ..forms import ContactForm


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


# def test_send_email(client):
#     test_data = {'title': 'test title',
#                  'message': 'test message',
#                  'email_from': 'testmail@mail.com'}
#     response = client.post('/contact-us/', data=test_data)
#     assert response.status_code == 302
