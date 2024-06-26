"""
URL configuration for itclub_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from itclub import views
from itclub_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('itclub.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
    # если в '' вписать префикс (напр. 'itclub/'), то он будет подставляться перед адресами в itclub.urls,
    #     т.е. станет '/itclub/'  и '/itclub/groups/' соответственно.
]

if settings.DEBUG:  # необходимо только в режиме отладки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404=views.page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Статьи учеников ITclub"