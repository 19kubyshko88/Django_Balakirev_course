from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000/
    path('groups/<int:groups_id>/', views.groups, name='groups_id'),  # http://127.0.0.1:8000/groups/number
    path('groups/<slug:groups_slug>/', views.groups_by_slug, name='groups_slug'),  # http://127.0.0.1:8000/groups/numb-and-let
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive)
    path('archive/<year4:year>/', views.archive, name='archive')
]
