import os
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Location, Image
import json


def get_detailsUrl(location):
    details_filename = f'places/static/places/places/{location.properties_placeId}.json'

    imgs = Image.objects.filter(location=location)
    details_url = {
        "title": location.title,
        "imgs": [img.image.url for img in imgs],
        "description_short": location.description_short,
        "description_long": location.description_long,
        "coordinates": {
            "lng": float(location.lng),
            "lat": float(location.lat)
        }
    }
    if not os.path.isfile(details_filename):
        with open(details_filename, 'w') as f:
            f.write(json.dumps(details_url, ensure_ascii=False, indent=4))
    return details_url


def convert_to_geojson(location):
    get_detailsUrl(location)
    geo_dict = \
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(location.lng), float(location.lat)]
            },
            "properties": {
                "title": location.properties_title,
                "placeId": location.properties_placeId,
                "detailsUrl": f'static/places/places/{location.properties_placeId}.json'
            }
        }
    return geo_dict


def index(request):
    context = {}
    query = Location.objects.all()

    locations = {
      "type": "FeatureCollection",
      "features": [convert_to_geojson(location) for location in query]
    }
    context['locations'] = json.dumps(locations, ensure_ascii=False)

    return render(request, 'places/index.html', context)


def json_api(request, pk):
    location = get_object_or_404(Location, id=pk)
    return JsonResponse(get_detailsUrl(location), json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })
