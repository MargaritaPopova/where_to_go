from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField(max_length=1000)
    description_long = models.TextField()
    lng = models.DecimalField(max_digits=17, decimal_places=14)
    lat = models.DecimalField(max_digits=17, decimal_places=14)

    def __str__(self):
        return self.title
