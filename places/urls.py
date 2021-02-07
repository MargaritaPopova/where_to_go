from django.urls import path
from places import views

app_name = 'places'

urlpatterns = [
    path('', views.index),
    path('places/<int:pk>', views.json_api, name="location_json")
]
