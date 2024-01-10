from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView

from .forms import LoginUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):  # можно использовать для изменения автоматического перенаправление в профайл
    #     return reverse_lazy('home')
