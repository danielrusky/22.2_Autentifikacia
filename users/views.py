import secrets
import string

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


def confirm_email(request):
    """подтверждаем почту"""
    confirm_user_email(request, request.user)
    return redirect(reverse('users:profile'))


def activate_email(request, key):
    """активируем почту"""
    print(request.user.email_confirm_key, key, sep='\n')
    if request.user.email_confirm_key == key:
        request.user.email_is_confirmed = True
        request.user.email_confirm_key = None
        request.user.save()
    else:
        print('Ключ не актуален')
    return redirect('/')


def password_reset(request):
    """генерируем пароль для неавторизованного пользователя"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = create_secret_key(12)
            user.set_password(new_password)
            user.save()
            login(request, user)

            send_mail(
                subject='Вы сменили пароль',
                message=f'Новый пароль {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email]
            )

            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/password_reset_form.html',
                          {'error_message': 'Такого пользователя не существует'})
    return render(request, 'users/password_reset_form.html')


def create_secret_key(length):
    """создаем ключ"""
    combination = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(combination) for _ in range(length))
    return secret_key


def confirm_user_email(request, user):
    """ссылка + письмо для подтверждения почты"""
    secret_key = create_secret_key(30)
    user.email_confirm_key = secret_key
    user.save()

    current_site = get_current_site(request)
    message = render_to_string('users/confirm_email_message.html', {
        'domain': current_site.domain,
        'key': secret_key,
    })
    send_mail(
        subject='Подтверждение почты',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def generate_password(request):
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
