# from django.db import models
# from django.db.models import fields
# from django import forms
from django.forms import ModelForm, NumberInput, TextInput

from .models import Student


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'surname', 'age', 'phone']
        widgets = {
            'name': TextInput(attrs={
                'type': 'text',
                'placeholder': 'Name',
                'size': '25',
                'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
                ),
            'surname': TextInput(attrs={
                'type': 'text',
                'placeholder': 'Surname',
                'size': '25',
                'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
                ),
            'age': NumberInput(attrs={
                'placeholder': '20',
                'style': 'margin-bottom: 5px; padding: 4px 10px; border-radius: 5px'}
                ),
            'phone': TextInput(attrs={
                'type': 'text',
                'placeholder': 'Phone',
                'size': '20',
                'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
                ),
        }


# class ContactForm(forms.Form):
#     title = forms.CharField(label='title', max_length=100, widget=forms.TextInput(attrs={
#         'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
#         'placeholder': 'Title',
#         'size': '30'}))
#     message = forms.CharField(label='message', max_length=250, widget=forms.Textarea(attrs={
#         'rows': 5, 'cols': 30,
#         'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
#         'placeholder': 'Message'}))
#     email_from = forms.EmailField(label='email_from', max_length=100, widget=forms.EmailInput(attrs={
#         'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
#         'placeholder': 'Email@',
#         'size': '30'}))
