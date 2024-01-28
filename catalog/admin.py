from django.contrib import admin

from catalog.models import Category, Product, Version, Contacts
from users.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'version_number', 'product', 'is_current')


admin.site.register(Contacts)

admin.site.register(User)
