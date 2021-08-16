from django import forms


class GroupForm(forms.Form):
    subject = forms.CharField(label='subject', max_length=200, widget=forms.TextInput(attrs={
        'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
        'placeholder': 'Subject',
        'size': '25'}))
    ratio_of_students = forms.IntegerField(label='ratio_of_students', widget=forms.NumberInput(attrs={
        'style': 'margin-bottom: 5px; padding: 4px 10px; border-radius: 5px',
        'placeholder': 'Student numbers'}))
