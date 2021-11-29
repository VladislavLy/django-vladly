from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'type': 'text',
            'placeholder': 'Name', 'size': '20',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
            'placeholder': 'Email@',
            'size': '20'}))
    password1 = forms.CharField(label='Password first time', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password first time',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}))
    password2 = forms.CharField(label='Password second time', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password second time',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. "
                                        "Please supply a different email address.")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Your username', widget=forms.TextInput(
        attrs={
            'type': 'text',
            'placeholder': 'Your username',
            'size': '20',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}))
    password = forms.CharField(label='Your password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Your password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}))

    class Meta:
        model = User
        fields = ["username", "password"]


class PasswordUserChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Current password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Current password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
            ))
    new_password1 = forms.CharField(label='New password', max_length=100, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'New password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
            ))
    new_password2 = forms.CharField(label='Confirm new password', max_length=100, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm new password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'}
            ))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class SetPasswordUserForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', max_length=100, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'New password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'},
            ))
    new_password2 = forms.CharField(label='Confirm new password', max_length=100, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm new password',
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px'},
            ))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=100, label='Email', widget=forms.EmailInput(
        attrs={
            'style': 'margin-bottom: 5px; padding: 7px 7px; border-radius: 5px',
            'placeholder': 'Email@',
            'size': '20'},
            ))

    class Meta:
        model = User
        fields = ("email")
