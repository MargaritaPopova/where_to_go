"""
Функции обработки запросов

"""
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Location


def get_detailsUrl_field(location):
    """

    Возвращает словарь с данными о локации в нужном формате для поля detailsUrl в данных geo-json

    :param location: объект Location

    :return: dictionary

    """
    imgs = location.images.all()
    details_url_data = {
        "title": location.title,
        "imgs": [img.image.url for img in imgs],
        "description_short": location.short_description,
        "description_long": location.long_description,
        "coordinates": {
            "lng": location.lng,
            "lat": location.lat
        }
    }
    return details_url_data


def convert_to_geojson(location):
    """

    Возвращает словарь с данными geo-json для конкретной локации

    :param location: Объект Location

    :return: dictionary

    """
    location_serialized = \
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location.lng, location.lat]
            },
            "properties": {
                "title": location.properties_title,
                "placeId": location.properties_placeId,
                "detailsUrl": reverse('places:location_json', kwargs={'pk': location.id})
            }
        }
    return location_serialized


def index(request):
    """

    Формирует список локаций в формате geo-json и рендерит его на страницу

    :param request: request

    :return: HTTP Response со списком локаций в теге <script>

    """
    context = {}
    all_locations = Location.objects.all()

    context['locations'] = {
      "type": "FeatureCollection",
      "features": [convert_to_geojson(location) for location in all_locations]
    }

    return render(request, 'places/index.html', context)


def json_api(request, pk):
    """

    Возвращает json для поля detailsUrl каждой локации

    :param request: request
    :param pk: id локации

    :return: JsonResponse

    """
    location = get_object_or_404(Location, id=pk)
    return JsonResponse(get_detailsUrl_field(location), json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })
