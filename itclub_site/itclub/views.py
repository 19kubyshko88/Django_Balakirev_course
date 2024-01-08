from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .utils import DataMixin
from .models import StudentArticles, Category, TagPost, Summary, UploadFiles
from .forms import AddPostForm, UploadFileForm

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# def index(request):
#     posts = StudentArticles.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'itclub/index.html', context=data)


class ArticlesHome(DataMixin, ListView):
    template_name = 'itclub/index.html'
    context_object_name = 'posts'  # для замены имени object_list на posts, чтобы не менять в index.html
    title_page = 'Главная страница'
    cat_selected = 0
    # extra_context = {  # определяет статические (известные) данные (не из GET-запроса)
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'cat_selected': 0,
    # }

    def get_queryset(self):  # оставляем только опубликованные статьи
        return StudentArticles.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = StudentArticles.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


def about(request):  # пропустить
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'itclub/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


# def show_post(request, post_slug):
#     post = get_object_or_404(StudentArticles, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'itclub/post.html', context=data)


class ShowPost(DataMixin, DetailView):
    template_name = 'itclub/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'  # чтобы вместо object в post.html подставлялась переменная post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):  # чтобы нельзя было вручную вбить адрес поста и увидеть его.
        return get_object_or_404(StudentArticles.published, slug=self.kwargs[self.slug_url_kwarg])

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {'title': 'Добавление страницы',
#             'menu': menu,
#             'form': form,
#             }
#     return render(request, 'itclub/addpage.html', data)


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm  # класс формы для заполнения. Без вызова (!), т.е. без скобок!
    template_name = 'itclub/addpage.html'  # по умолчанию в шаблон форма передаётся через переменную form.
    # Куда отправит после успешного заполнения формы
    # success_url = reverse_lazy('home')  # lazy чтобы маршрут строился не сразу, а только когда необходим. лучше чем reverse.
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = StudentArticles
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'itclub/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {'title': 'Добавление страницы',
#                 'menu': menu,
#                 'form': form,
#                 }
#         return render(request, 'itclub/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {'title': 'Добавление страницы',
#                 'menu': menu,
#                 'form': form,
#                 }
#         return render(request, 'itclub/addpage.html', data)

class DeletePage(DataMixin, DeleteView):
    model = StudentArticles
    success_url = reverse_lazy("home")
    title_page = 'Удаление статьи'



def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = StudentArticles.published.filter(cat_id=category.pk).select_related('cat')
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'itclub/index.html', context=data)


class ArticlesByCategory(DataMixin, ListView):
    template_name = 'itclub/index.html'
    context_object_name = 'posts'
    allow_empty = False  # для генерации ошибки 404 при неверном слаге в url.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,
                                      )

    def get_queryset(self):
        return StudentArticles.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # cst_slug из urls


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.articles.filter(is_published=StudentArticles.Status.PUBLISHED).select_related('cat')
#     data = {
#         'title': f'Тег: {tag.tag_name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'itclub/index.html', context=data)


class ArticlesByTag(DataMixin, ListView):
    template_name = 'itclub/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag_name)

    def get_queryset(self):
        return StudentArticles.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def groups(request, groups_id):  # request  это HttpRequest
    return HttpResponse(f"<h1>Группы</h1><p>ID: {groups_id}</p>")


def groups_by_slug(request, groups_slug):  # request  это HttpRequest
    if request.GET:  # http://127.0.0.1:8000/groups/3d/?day=tuesday&class=1
        print(request.GET)  # То же request.POST
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
        uri = reverse('groups_slug', args=('Scratch',))
        return HttpResponsePermanentRedirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")
