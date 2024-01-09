from itclub.utils import menu


def get_itclub_site_context(request):
    return {'mainmenu': menu}  # переменная mainmenu будет доступна во всех шаблонах
