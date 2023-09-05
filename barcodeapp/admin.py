from django.contrib import admin

from .models import Barcode
@admin.register(Barcode)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('code', 'image')
# Register your models here.

