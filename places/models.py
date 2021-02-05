from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название для боковой панели')
    description_short = models.TextField(max_length=1000)
    description_long = models.TextField()
    lng = models.CharField(max_length=30)
    lat = models.CharField(max_length=30)
    properties_title = models.CharField(max_length=200, default='', verbose_name='Название для точки')
    properties_placeId = models.CharField(max_length=200, default='', verbose_name='Уникальный идентификатор локации')

    def __str__(self):
        return self.title


class Image(models.Model):
    order_no = models.SmallIntegerField()
    image = models.ImageField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image {self.order_no} for {self.location}'
