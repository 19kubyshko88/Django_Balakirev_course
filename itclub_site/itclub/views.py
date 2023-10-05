from django.http import HttpResponse
from django.shortcuts import render


def index(request): # request  это HttpRequest
    return HttpResponse("Страница ITclub")


def groups(request): # request  это HttpRequest
    return HttpResponse( "<h1>Группы</h1>")