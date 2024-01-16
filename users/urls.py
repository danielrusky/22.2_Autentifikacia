from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, UserDetailView, confirm_email, activate_email, password_reset, \
    generate_new_password, VerifyEmailView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/view', ProfileView.as_view(), name='profile_view'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('verify_email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),


    path('confirm', confirm_email, name='confirm'),
    path('activate<str:key>', activate_email, name='activate'),
    path('password_reset/', password_reset, name='password_reset')
    ]