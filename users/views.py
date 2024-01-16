import secrets
import string

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, PasswordResetForm
from users.models import User
from django.conf import settings


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        token = default_token_generator.make_token(new_user)
        new_user.verification_code = token
        new_user.save()
        activation_url = reverse_lazy('users:verify_email', kwargs={'token': token})
        send_mail(
            subject='Активация аккаунта на нашей платформе',
            message=f'Ссылка для активации учетной записи: http://127.0.0.1:8000{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class VerifyEmail(View):
    def get(self, request, token):
        try:
            user = User.objects.get(verification_code=token)
            user.is_active = True
            user.save()
            return redirect('users:success_verify')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return redirect('users:error_verify')


class SuccessVerifyView(TemplateView):
    template_name = 'users/success_verify.html'


class ErrorVerifyView(TemplateView):
    template_name = 'users/error_verify.html'


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = create_secret_key(12)
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Вы сменили пароль из профиля',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse_lazy('users:login'))


def create_secret_key(length):
    """создаем ключ"""
    combination = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(combination) for _ in range(length))
    return secret_key