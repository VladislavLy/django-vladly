from django.forms import ModelForm, NumberInput, TextInput

from .models import Teacher


class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'age']
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
        }
