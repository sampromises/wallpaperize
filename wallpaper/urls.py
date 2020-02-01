from django.conf.urls import url

from wallpaper import views

urlpatterns = \
    [
        url(r'^$', views.index, name='index'),
    ]
