from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    # path('register/', views.RegisterUser.as_view(), name='register'),
    # path('register/', views.register_user_view, name='register'),
    path('register/', views.SignupUser.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('login/', views.login_user_view, name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    # path('logout/', views.logout_user_view, name='logout'),
    path('password-change/', views.PasswordChangeUser.as_view(), name='password_change'),
    # path('password-change/', views.change_password_user_view, name='password_change'),
    path('password-change-success/', auth_views.PasswordChangeDoneView.as_view(
        template_name='signup/password_change_done.html'),
        name='password_change_done'),
    path('reset-password/', views.PasswordResetUser.as_view(), name='reset_password'),
    # path('reset-password/', views.password_reset_user_view, name='reset_password'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='signup/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmUser.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='signup/password_reset_complete.html'),
        name='password_reset_complete')

]
