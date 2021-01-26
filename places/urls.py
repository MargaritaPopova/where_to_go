from django.urls import path
from .views import index

app_name = 'places'

urlpatterns = [
    path('', index),
]
