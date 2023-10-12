from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):  # request  это HttpRequest
    # return HttpResponse('''<!DOCTYPE html>
    # <html>
    # <head>
    #          <title>Мой заголовок</title>
    # </head>
    # <body>
    #  <h1>Привет, мир!</h1>
    # </body>
    # </html>''')
    # t = render_to_string('itclub/index.html')
    # return HttpResponse(t)
    data = {'title': "главная стр?аница ITclub",
            'main_title': "",
            'menu': menu,
            'float': 28.57,
            'lst': [1, 2, 'abc', True],
            'set': {1, 1, 2, 3, 2, 5},
            'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
            'obj': MyClass(10, 20),
            'url': slugify('Slugify from Python')
            }
    return render(request, 'itclub/index.html', context=data)


def about(request):
    data = {'title': "О сайте ITclub"}
    return render(request, 'itclub/about.html', data)


def groups(request, groups_id):  # request  это HttpRequest
    return HttpResponse(f"<h1>Группы</h1><p>ID: {groups_id}</p>")


def groups_by_slug(request, groups_slug):  # request  это HttpRequest
    if request.GET:         # http://127.0.0.1:8000/groups/3d/?day=tuesday&class=1
        print(request.GET)   # То же request.POST
    return HttpResponse(f"<h1>Группы</h1><p>Slug: {groups_slug}</p>")


def archive(request, year):
    print(year, type(year))
    if year > 2023:
        # raise Http404()
        # return redirect('/', permanent=True)
        # return redirect(index)
        # return redirect('home')
        # return redirect('groups_slug', '3D')
        # uri = reverse('groups', args=('3D', ))
        # return redirect(uri)
        # return HttpResponseRedirect('/')
        uri = reverse('groups_slug', args=('Scratch', ))
        return HttpResponsePermanentRedirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')