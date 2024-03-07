from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .utils import DataMixin
from .models import StudentArticles, Category, TagPost, Summary, UploadFiles
from .forms import AddPostForm, UploadFileForm

from django.db.models.signals import pre_save


class ArticlesHome(DataMixin, ListView):
    template_name = 'itclub/index.html'
    context_object_name = 'posts'  # для замены имени object_list на posts, чтобы не менять в index.html
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):  # оставляем только опубликованные статьи
        return StudentArticles.published.all().select_related('cat')


def about(request):  # пропустить
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'itclub/about.html', {'title': 'О сайте', 'form': form})


class ShowPost(DataMixin, DetailView):
    template_name = 'itclub/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'  # чтобы вместо object в post.html подставлялась переменная post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):  # чтобы нельзя было вручную вбить адрес поста и увидеть его.
        return get_object_or_404(StudentArticles.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # класс формы для заполнения. Без вызова (!), т.е. без скобок!
    template_name = 'itclub/addpage.html'  # по умолчанию в шаблон форма передаётся через переменную form.
    title_page = 'Добавление статьи'
    permission_required = 'itclub.add_studentarticles'
    # login_url = '/admin/' # ели хотим перебить LOGIN_URL из settings

    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = self.request.user
        pre_save.send(sender=StudentArticles, instance=a, form=form)
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = StudentArticles
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'itclub/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'itclub.change_studentarticles'


class DeletePage(DataMixin, DeleteView):
    model = StudentArticles
    success_url = reverse_lazy("home")
    title_page = 'Удаление статьи'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ArticlesByCategory(DataMixin, ListView):
    template_name = 'itclub/index.html'
    context_object_name = 'posts'
    allow_empty = False  # для генерации ошибки 404 при неверном слаге в url.

    def get_queryset(self):
        return StudentArticles.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,
                                      )



def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


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
