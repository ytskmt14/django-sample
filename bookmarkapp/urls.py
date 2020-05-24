from django.urls import path

from . import views

app_name = 'bookmarkapp'
urlpatterns = [
  path('', views.index, name='index'),
  path('detail/<int:pk>', views.detail, name='detail'),
  path('detail', views.detail, name='detail'),
  path('top_create', views.top_create, name='top_create'),
  # path('detail_create', views.detail_create, name='detail_create'),
  # path('sub_detail_create', views.sub_detail_create, name='sub_detail_create'),
]
