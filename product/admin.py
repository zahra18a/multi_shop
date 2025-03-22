from django.contrib import admin
from . import models

class InformationAdmin(admin.StackedInline):
    model = models.InformationalProduct

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = [InformationAdmin]


admin.site.register(models.Size)
admin.site.register(models.Color)
