from django.contrib import admin
from .models import Customer

# Register your models here.
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)
    fields = ('email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active' )

admin.site.register(Customer, CustomerModelAdmin)
