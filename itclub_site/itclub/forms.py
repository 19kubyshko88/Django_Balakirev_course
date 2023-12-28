from django import forms
from .models import Category, Summary


class AddPostForm(forms.Form):
    """
    класс, описывающий форму добавления статьи
    """
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    summary = forms.CharField(widget=forms.Textarea(), required=False, label="Резюме")
