from django.contrib import admin
from .models import TopListModel, DetailListModel, SubDetailListModel, DetailWork

# Register your models here.

admin.site.register(TopListModel)
admin.site.register(DetailListModel)
admin.site.register(SubDetailListModel)
admin.site.register(DetailWork)
