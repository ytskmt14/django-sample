from django.urls import path
from django.contrib.staticfiles.urls import static
import sys
sys.path.append('../')
from config import settings

from . import views

app_name = 'bookmarkapp'
urlpatterns = [
  path('travels', views.index, name='index'),
  path('travels/<int:pk>', views.detail, name='detail'),
  path('travels/create', views.top_create, name='top_create'),
  path('travels/<int:pk>/edit', views.top_update, name='top_update'),
  path('travels/<int:pk>/delete', views.top_delete, name='top_delete'),
  path('travels/<int:pk>/plans/create', views.detail_create, name='detail_create'),
  path('travels/<int:top_pk>/plans/<int:detail_pk>/create', views.sub_detail_create, name='sub_detail_create'),
  path('travels/<int:top_pk>/plans/<int:pk>/edit', views.detail_update, name='detail_update'),
  path('travels/<int:top_pk>/plans/<int:pk>/delete', views.detail_delete, name='detail_delete'),
  path('travels/<int:top_pk>/plans/<int:pk>/schedules/edit', views.sub_detail_update, name='sub_detail_update'),
  path('travels/<int:top_pk>/plans/<int:pk>/schedules/delete', views.sub_detail_delete, name='sub_detail_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)