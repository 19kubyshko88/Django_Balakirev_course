from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=StudentArticles.Status.PUBLISHED)


class StudentArticles(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    # 'Category'- строка, т.к. класс Category опередлен после StudentArticles. Если перед, то можно без кавычек.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='articles')
    summary = models.OneToOneField('Summary', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_post')

    published = PublishedModel()
    objects = models.Manager()  # после published objects надо переопределять, иначе не будет такого поля.

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

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

    def __str__(self):
        return self.summary_text[:50]
