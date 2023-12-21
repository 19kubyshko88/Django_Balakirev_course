from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=StudentArticles.Status.PUBLISHED)


class StudentArticles(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    # 'Category'- строка, т.к. класс Category опередлен после StudentArticles. Если перед, то можно без кавычек.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='articles', verbose_name="Тэги")
    summary = models.OneToOneField('Summary', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='related_post', verbose_name="Резюме")

    published = PublishedModel()
    objects = models.Manager()  # после published objects надо переопределять, иначе не будет такого поля.

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья ученика'
        verbose_name_plural = 'Статьи учеников'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Summary(models.Model):
    summary_text = models.TextField(blank=True)
    post_length = models.IntegerField(null=True)
    update_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.summary_text[:50]
