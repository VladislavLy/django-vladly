import os
import socket

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.core.mail import BadHeaderError, send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import CreateView

from mysite.settings import EMAIL_HOST_USER

from .forms import LoginUserForm, PasswordUserChangeForm, RegisterUserForm, SetPasswordUserForm, UserForgotPasswordForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'signup/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        users_name = form.cleaned_data.get('username')
        messages.success(self.request, 'Account was created for ' + users_name + '!')
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'signup/login.html'

    def get_success_url(self):
        messages.success(self.request, "You've logged in successfully!")
        if 'next' in self.request.POST:
            redirect_to = self.request.POST.get('next')
            return redirect_to
        else:
            return reverse_lazy('index')


class LogoutUser(LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(self.request, "You've logged out successfully!")
        return super().dispatch(request, *args, **kwargs)


def login_user_view(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've logged in successfully!")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = LoginUserForm()
    context = {'form': form}
    return render(request, 'signup/login.html', context)


def logout_user_view(request):
    logout(request)
    messages.info(request, "You've logged out successfully!")
    return redirect('index')


def register_user_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account was created for ' + username + '!')
            return redirect('index')
    else:
        form = RegisterUserForm()
    context = {'form': form}
    return render(request, 'signup/register.html', context)


class PasswordChangeUser(PasswordChangeView):
    form_class = PasswordUserChangeForm
    template_name = "signup/password_change_form.html"
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your password has been changed successfully!')
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


def change_password_user_view(request):
    if request.method == 'POST':
        form = PasswordUserChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('password_change_done')
        # else:
        #     messages.error(request, 'Old password was entered incorrectly...')
    else:
        form = PasswordUserChangeForm(request.user)
    return render(request, 'signup/password_change_form.html', {'form': form})


class PasswordResetUser(PasswordResetView):
    form_class = UserForgotPasswordForm
    title = 'Password resetdasdas'
    from_email = f'DJANGO_VLADLY {EMAIL_HOST_USER}'
    template_name = 'signup/password_reset.html'
    email_template_name = 'signup/password_reset_email.html'
    subject_template_name = 'signup/reset_subject.txt'

    def form_valid(self, form):
        data = form.cleaned_data['email']
        associated_user = User.objects.filter(Q(email=data))
        if not associated_user.exists():
            messages.error(self.request, 'The invalid email has been entered!')
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class PasswordResetConfirmUser(PasswordResetConfirmView):
    form_class = SetPasswordUserForm
    template_name = 'signup/password_reset_confirm.html'


def password_reset_user_view(request):
    if socket.gethostname().endswith(".local"):
        domain = '127.0.0.1:8000'
    else:
        domain = 'django-site-vladly.herokuapp.com'

    if request.method == "POST":
        password_reset_form = UserForgotPasswordForm(request.POST)

        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=data))

            if associated_user.exists():
                for user in associated_user:
                    subject = "Password Reset"
                    email_template_name = "signup/reset_password_email.txt"
                    parameters = {
                        'email': user.email,
                        'domain': domain,
                        'site_name': 'Website',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        'user': user,
                    }
                    email = render_to_string(email_template_name, parameters)
                    from_email = os.getenv('EMAIL_HOST_USER')
                    try:
                        send_mail(subject, email, from_email, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header!')
                    return redirect("password_reset_done")

            messages.error(request, 'The invalid email has been entered!')
        messages.error(request, 'The invalid email has been entered!')

    password_reset_form = UserForgotPasswordForm()
    return render(request=request, template_name="signup/password_reset.html", context={"form": password_reset_form})
