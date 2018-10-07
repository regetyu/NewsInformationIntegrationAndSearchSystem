"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from mysite import view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',view.homepage),
    url(r'^search_form$',view.search_form),
    url(r'^show/(\d+)$',view.show),
    url(r'^search$',view.search),
    url(r'^page/(\d+)$',view.page),
    url(r'^search/([^/]+?)/(\d+)$',view._search),
    url(r'^time_search_form$',view.time_search_form),
    url(r'^time_search$',view.time_search),
    url(r'^time_search/([^/]+?)/([^/]+?)/(\d+)$',view._time_search),
    url(r'^multi_search_form/$',view.multi_search_form),
    url(r'^multi_search$',view.multi_search),
    url(r'^multi_search/([^/]+?)/(\d+)$',view._multi_search),
]
