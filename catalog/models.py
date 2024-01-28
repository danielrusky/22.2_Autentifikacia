from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='Поле_для_дальнейшего_удаления', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена', default=0)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_modified = models.DateTimeField(verbose_name='Дата последнего изменения', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='в наличие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=50, verbose_name='название версии')
    is_current = models.BooleanField(default=False, verbose_name='признак текущаей версии')
    is_active = models.BooleanField(default=True, verbose_name='активна версия')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class VersionCategory(models.Model):
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=50, verbose_name='название версии')
    is_current = models.BooleanField(default=False, verbose_name='признак текущаей версии')
    is_active = models.BooleanField(default=True, verbose_name='активна версия')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    phone = models.IntegerField(unique=True, null=False, blank=False)
    message = models.TextField(verbose_name='message')

    def __str__(self):
        return f"{self.name}({self.phone})"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


def toggle_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_active:
        product_item.is_active = False
    else:
        product_item.is_active = True

    product_item.save()

    return redirect(reverse('home'))
