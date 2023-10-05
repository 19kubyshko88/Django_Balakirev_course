from django.urls import path
from itclub import views

urlpatterns = [
    path('',views.index), # http://127.0.0.1:8000/
    path('groups/',views.groups), # http://127.0.0.1:8000/groups/
]