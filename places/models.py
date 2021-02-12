from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Location(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название для боковой панели')
    description_short = models.TextField(max_length=1000, verbose_name='Краткое описание')
    description_long = HTMLField(verbose_name='Полное описание', max_length=10000)
    lng = models.CharField(max_length=30, verbose_name='Долгота')
    lat = models.CharField(max_length=30, verbose_name='Широта')
    properties_title = models.CharField(max_length=200, default='', verbose_name='Название точки на карте')
    properties_placeId = models.CharField(max_length=200, default='', verbose_name='Уникальный идентификатор локации')

    def __str__(self):
        return self.title


class Image(models.Model):
    order_no = models.SmallIntegerField(default=0, blank=False, null=False)
    image = models.ImageField(verbose_name='Файл')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['order_no']

    def __str__(self):
        return f'Image {self.order_no} for {self.location}'

    def preview(self):
        return format_html("<img src={} height={}/>",
                           self.image.url,
                           200,
                           )

