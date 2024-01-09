from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):  # можно использовать для изменения автоматического перенаправление в профайл
    #     return reverse_lazy('home')


def logout_user(request):
    return HttpResponse("logout")
