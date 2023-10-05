from django.http import HttpResponse
from django.shortcuts import render


def index(request):  # request  это HttpRequest
    return HttpResponse("Страница ITclub")


def groups(request, groups_id):  # request  это HttpRequest
    return HttpResponse(f"<h1>Группы</h1><p>ID: {groups_id}</p>")


def groups_by_slug(request, groups_slug):  # request  это HttpRequest
    return HttpResponse(f"<h1>Группы</h1><p>Slug: {groups_slug}</p>")


def archive(request, year):
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")
