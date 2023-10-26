from django import template
import itclub.views as views

register = template.Library() # для регистрации новых тегов


@register.simple_tag(name='getcats')
def get_categories():
    return views.cats_db


@register.inclusion_tag('itclub/list_categories.html')
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {"cats": cats}