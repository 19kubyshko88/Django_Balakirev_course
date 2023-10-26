from django import template
import itclub.views as views

register = template.Library() # для регистрации новых тегов


@register.simple_tag()
def get_categories():
    return views.cats_db
