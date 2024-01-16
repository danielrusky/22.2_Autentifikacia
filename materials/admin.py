from materials.models import Material
from django.contrib import admin


# Register your models here.
@admin.register(Material)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count',)
    list_filter = ('is_published', 'views_count',)
    search_fields = ('title', 'body',)
