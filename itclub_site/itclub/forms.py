from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import Category, Summary, StudentArticles
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


class AddPostForm(forms.ModelForm):
    """
    класс, описывающий форму добавления статьи
    """
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")

    class Meta:
        model = StudentArticles
        fields = ['title', 'slug', 'content', 'is_published', 'cat','tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}), # css стиль
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
