"""
Модели данных для локаций и картинок.

:Location: Точка на карте
:Image: Картинка для конкретной точки

"""
import uuid

from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Location(models.Model):
    """
    Представление данных локации

    Attributes
    ----------
    :title: :str
        Название места, строковое поле CharField
    :short_description: :str
        Короткое описание, строковое поле CharField
    :long_description: :str
        Полное описание, поле HTMLField с поддержкой форматирования
    :lng: :str
        Долгота, поле FloatField
    :lat: :str
        Широта, поле FloatField
    :properties_title: :str
        Название для поля properties, строковое поле CharField
    :properties_placeId: :uuid
        Уникальный идентификатор локации, поле UUIDField

    Methods
    -------
    :__str__(self):
        Возвращает строковое представление модели

    """
    title = models.CharField(max_length=200, verbose_name='Название для боковой панели', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', blank=True)
    long_description = HTMLField(verbose_name='Полное описание', blank=True)
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')
    properties_title = models.CharField(max_length=200, default='', verbose_name='Название точки на карте')
    properties_placeId = models.UUIDField(
        default=uuid.uuid4, editable=False, verbose_name='Уникальный идентификатор локации'
    )

    def __str__(self):
        return self.title


class Image(models.Model):
    order_no = models.SmallIntegerField(default=0, null=True)
    image = models.ImageField(verbose_name='Файл')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='images')

    class Meta(object):
        ordering = ['order_no']

    def __str__(self):
        return f'Image for {self.location}'

    def preview(self):
        """
        Метод для отображения миниатюр фото в панели администрирования

        :return: html с тегом <img> и заданным стилем (макс. высота 200px)

        """
        return format_html("<img src={} height={}/>", self.image.url, 200)

