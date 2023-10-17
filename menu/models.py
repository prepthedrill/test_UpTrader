from django.db import models


class Menu(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Название меню',
        help_text='Придумайте название меню'
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name='Меню',
        help_text='Выберите меню из списка',
        related_name='items'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Родитель',
        help_text='Выберите родителя из списка',
        related_name='items'
    )
    title = models.CharField(
        max_length=32,
        verbose_name='Заголовок пункта меню',
        help_text='Придумайте Заголовок пункта меню'
    )
    slug = models.SlugField(
        max_length=16,
        unique=True,
        verbose_name='URL адрес для пункта меню',
        help_text='Придумайте уникальный URL адрес для пункта меню'
    )

    def __str__(self):
        return self.title
