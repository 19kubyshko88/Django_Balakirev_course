from django import forms
from .models import Category, Summary
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddPostForm(forms.Form):
    """
    класс, описывающий форму добавления статьи
    """
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка - никак',
                            })
    slug = forms.SlugField(max_length=255, label="URL", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    summary = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),  required=False, label="Резюме")
