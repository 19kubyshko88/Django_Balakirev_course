from django import template
import itclub.views as views

from itclub.models import Category

register = template.Library() # для регистрации новых тегов


@register.inclusion_tag('itclub/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}