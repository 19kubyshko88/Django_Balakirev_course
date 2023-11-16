from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect,  get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify

from .models import StudentArticles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h3>Проект Анджелины</h3> lorem150 ipsum dolor sit amet,\
    consectetur adipisicing elit. 
    Alias aliquam animi commodi doloribus ducimus earum, expedita fugit, inventore ipsum\
     nisi perspiciatis praesentium quia, quos veritatis vitae. Ab aliquid, deleniti deserunt dolores optio ratione \
     suscipit? Atque eum fuga harum nesciunt quidem! Animi exercitationem molestiae soluta! Ab accusamus consectetur \
     eligendi et in, laudantium maxime officiis pariatur sapiente sequi vero voluptate voluptatum. Aut deleniti \
     doloribus explicabo id libero minima molestias nihil officiis perferendis quibusdam quo quod sunt tempore \
     temporibus, voluptatem. Aspernatur deleniti distinctio enim, eveniet harum id ipsa ipsum iste, laboriosam libero\
     natus praesentium provident qui quibusdam ratione reiciendis rerum. Autem, nesciunt repellat.''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Проект Марго Робби', 'is_published': True},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Проект Джулия Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': '1 год'},
    {'id': 2, 'name': '2 год'},
    {'id': 3, 'name': '3 год'},
]


def index(request):
    posts = StudentArticles.objects.filter(is_published=1)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'itclub/index.html', context=data)


def about(request):
    data = {'title': "О сайте ITclub"}
    return render(request, 'itclub/about.html', {'title':'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(StudentArticles, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'itclub/post.html', context=data)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'itclub/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


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
