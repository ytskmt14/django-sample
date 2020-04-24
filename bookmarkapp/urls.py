from django.urls import path

from . import views

app_name = 'bookmarkapp'
urlpatterns = [
  path('', views.index, name='index'),
]
