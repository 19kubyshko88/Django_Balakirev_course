from django.contrib import admin, messages
from .models import StudentArticles, Category


@admin.register(StudentArticles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 3
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = ['cat__name', 'is_published']

    @staticmethod
    @admin.display(description="Кол-во слов")
    def brief_info(st_article: StudentArticles):
        """
        Метод возвращает количество слов в статье.
        :param st_article:
        :return:
        """
        content: str = st_article.content
        return f"Количество слов: {len(content.split())}"

    @admin.action(description="Опубликовать записи")
    def set_published(self, request, queryset):
        queryset.update(is_published=StudentArticles.Status.PUBLISHED)
        count = queryset.update(is_published=StudentArticles.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=StudentArticles.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
