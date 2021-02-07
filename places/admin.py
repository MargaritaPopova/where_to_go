from django.contrib import admin
from .models import Location, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'preview', 'order_no')
    readonly_fields = ("preview", )


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Координаты', {'fields': ['lng', 'lat']}),
        ('Описание', {'fields': ['description_short', 'description_long']}),
        ('Идентификаторы', {'fields': ['properties_placeId', 'properties_title']}),
    ]
    inlines = [ImageInline]


admin.site.register(Location, LocationAdmin)
