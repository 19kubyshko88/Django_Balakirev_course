from django.contrib import admin
from .models import StudentArticles


@admin.register(StudentArticles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')


# admin.site.register(StudentArticles, ArticlesAdmin)
