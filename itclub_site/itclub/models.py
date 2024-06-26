from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model
# from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
import transliterate


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=StudentArticles.Status.PUBLISHED)


class StudentArticles(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, validators=[
                                                                                MinLengthValidator(5),
                                                                                MaxLengthValidator(100),
                                                                            ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=((bool(x[0]), x[1]) for x in Status.choices),
                                       default=Status.DRAFT, verbose_name="Статус")
    # 'Category'- строка, т.к. класс Category опередлен после StudentArticles. Если перед, то можно без кавычек.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='articles', verbose_name="Тэги")
    summary = models.OneToOneField('Summary', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='related_post', verbose_name="Резюме")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts',
                               null=True, default=None
                               )

    objects = models.Manager()  # в таком порядке, чтобы отображался статус в админпанели
    published = PublishedModel()

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
        if self.is_published:
            return reverse('post', kwargs={'post_slug': self.slug})
        else:
            return reverse('home')


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


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


@receiver(pre_save, sender=StudentArticles)  # сигнал: при отправке формы перед созданием статьи создать summary
def create_summary(sender, instance: StudentArticles, **kwargs):
    if instance.summary_id is None:
        form = kwargs.get('form')
        summary_text = form.cleaned_data.get('summary_text')
        instance.summary = Summary.objects.create(summary_text=summary_text, post_length=len(instance.content))
