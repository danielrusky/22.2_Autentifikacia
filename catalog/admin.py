from django.contrib import admin

from catalog.models import Product, Category, Contact, Version
from users.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'message')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'version_number', 'product', 'is_current')
    list_filter = ('version_name', 'version_number', 'product', 'is_current',)
    search_fields = ('version_name', 'version_number', 'product',)


admin.site.register(User)
