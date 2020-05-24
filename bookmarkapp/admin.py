from django.contrib import admin
from .models import TopListModel, DetailListModel, SubDetailListModel

# Register your models here.

admin.site.register(TopListModel)
admin.site.register(DetailListModel)
admin.site.register(SubDetailListModel)
