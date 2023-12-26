from django import forms
from .models import Category, Summary


class AddPostForm(forms.Form):
    """
    класс, описывающий форму добавления статьи
    """
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    summary = forms.CharField(widget=forms.Textarea(), required=False)
