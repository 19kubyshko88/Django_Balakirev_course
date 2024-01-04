from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import Category, Summary
import re

@deconstructible
class SimbolValidator:
    pattern = r'[А-Яа-яA-Za-z]+[\.?!-:\s]'
    code = 'valid_title'

    def __init__(self, message=None):
        self.message = message if message else "Допустимы русские/английские буквы, пробел и символы: .?-! и пробел."

    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.Form):
    """
    класс, описывающий форму добавления статьи
    """
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            # validators=[
                            #     SimbolValidator(),
                            # ],
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

    def clean_title(self):
        pattern = r'[А-Яа-яA-Za-z]+[\.?!-:\s]'
        title = self.cleaned_data['title']
        if not re.match(pattern, title):
            raise ValidationError("Допустимы русские/английские буквы, пробел и символы: .?-! и пробел.")
        return title
