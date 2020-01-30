from django.conf.urls import url

from converter import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
