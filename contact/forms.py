from django import forms


class ContactForm(forms.Form):
    title = forms.CharField(label='title', max_length=100, widget=forms.TextInput(attrs={
        'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
        'placeholder': 'Title',
        'size': '30'}))
    message = forms.CharField(label='message', max_length=250, widget=forms.Textarea(attrs={
        'rows': 5, 'cols': 30,
        'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
        'placeholder': 'Message'}))
    email_from = forms.EmailField(label='email_from', max_length=100, widget=forms.EmailInput(attrs={
        'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
        'placeholder': 'Email@',
        'size': '30'}))
