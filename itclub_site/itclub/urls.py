from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.ArticlesHome.as_view(), name='home'),  # http://127.0.0.1:8000/
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    # path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),  # сначала по id проще редактировать
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ArticlesByCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ArticlesByTag.as_view(), name='tag'),
    path('groups/<int:groups_id>/', views.groups, name='groups_id'),  # http://127.0.0.1:8000/groups/number
    path('groups/<slug:groups_slug>/', views.groups_by_slug, name='groups_slug'),  # http://127.0.0.1:8000/groups/numb-and-let
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive)
    path('archive/<year4:year>/', views.archive, name='archive'),
]
