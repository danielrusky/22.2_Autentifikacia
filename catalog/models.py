from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/', **NULLABLE)

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
    data_created = models.DateTimeField(verbose_name='Дата последнего изменения')

    is_active = models.BooleanField(default=True, verbose_name='в наличие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    phone = models.IntegerField(unique=True, null=False, blank=False)
    message = models.TextField(verbose_name='message')

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=50, verbose_name='название версии')
    is_current = models.BooleanField(default=False, verbose_name='признак текущаей версии')

    def __str__(self):
        return f'{self.version_name} - {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
