from django.contrib import admin

from .models import Item, Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    empty_value_display = '-пусто-'
