from django.urls import path

from . import views

app_name = 'bookmarkapp'
urlpatterns = [
  path('', views.index, name='index'),
  path('detail/<int:pk>', views.detail, name='detail'),
  path('top_create', views.top_create, name='top_create'),
  path('detail/<int:pk>/detail_create', views.detail_create, name='detail_create'),
  path('detail/<int:top_pk>/sub_detail_create/<int:detail_pk>', views.sub_detail_create, name='sub_detail_create'),
  path('top_update/<int:pk>', views.top_update, name='top_update'),
  path('detail/<int:top_pk>/detail_update/<int:pk>', views.detail_update, name='detail_update'),
  path('detail/<int:top_pk>/sub_detail_update/<int:pk>', views.sub_detail_update, name='sub_detail_update'),
  path('top_delete/<int:pk>', views.top_delete, name='top_delete'),
  path('detail/<int:top_pk>/detail_delete/<int:pk>', views.detail_delete, name='detail_delete'),
  path('detail/<int:top_pk>/sub_detail_delete/<int:pk>', views.sub_detail_delete, name='sub_detail_delete'),
]
