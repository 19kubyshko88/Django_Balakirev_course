from django.contrib import admin
from .models import StudentArticles, Category


@admin.register(StudentArticles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 3

    @staticmethod
    def brief_info(st_article: StudentArticles):
        """
        Метод возвращает количество слов в статье.
        :param st_article:
        :return:
        """
        content: str = st_article.content
        return f"Количество слов: {len(content.split())}"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
