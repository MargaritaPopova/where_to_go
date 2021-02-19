from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from .models import Location, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'preview', 'order_no')
    readonly_fields = ("preview",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('title',)}),
        ('Координаты', {'fields': ('lng', 'lat',)}),
        ('Описание', {'fields': ('short_description', 'long_description')}),
        ('Идентификаторы', {'fields': ('properties_title',)}),
    ]
    inlines = [ImageInline]
    search_fields = ['title']
