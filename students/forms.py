from django.forms import ModelForm, NumberInput, TextInput

from .models import Student


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'surname', 'age', 'phone', 'in_the_group']
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
            'in_the_group': TextInput(attrs={
                'type': 'text',
                'placeholder': 'In_the_group',
                'size': '20',
                'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
                ),
        }
