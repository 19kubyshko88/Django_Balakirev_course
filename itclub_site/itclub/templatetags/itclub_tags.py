from django import template
import itclub.views as views

from itclub.models import Category, TagPost

register = template.Library() # для регистрации новых тегов


@register.inclusion_tag('itclub/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('itclub/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}