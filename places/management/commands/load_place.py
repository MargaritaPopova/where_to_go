import os

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Location, Image


class Command(BaseCommand):
    """
    command: python manage.py load_place <link_to_json_file>
    Команда для заполнения данными локации на карте.
    Принимает аргументом ссылку на json-файл с описанием локации или файл со списком таких ссылок.
    Если объекта нет в базе данных, он будет создан.
    Если объект существует, скрипт обновляет поля из данных по ссылке (кроме картинок и названия).
    Если файл содержит данные в неверном формате, ссылка игнорируется.
    """
    help = 'Load location info from a link to json file or from file with list of links'

    def add_arguments(self, parser):
        parser.add_argument('source', type=str)

    def fill_data_from_link(self, link):
        response = requests.get(link.strip())
        if response.ok:
            location_data = response.json()
            if 'error' in location_data:
                raise requests.exceptions.HTTPError(location_data['error'])
            location, created = Location.objects.get_or_create(
                title=location_data['title'],
                defaults={
                    'lng': location_data['coordinates']['lng'],
                    'lat': location_data['coordinates']['lat'],
                    'long_description': location_data['description_long'],
                    'short_description': location_data['description_short'],
                    'properties_title': location_data['title']}
            )
            if created:
                for img in location_data['imgs']:
                    img_file = ContentFile(requests.get(img).content)
                    filename = img.split('/')[-1]
                    loc_img, created = Image.objects.get_or_create(
                        location_id=location.id,
                        image=filename
                    )
                    if created:
                        loc_img.image.save(filename, img_file, save=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully read file {link}'
                                                     f'Created Location object: {location.title} \n'))
            else:
                self.stdout.write(self.style.WARNING(f'Location {location.title} already exists, defaults updated.'))
        else:
            self.stdout.write(self.style.ERROR(f'Server returned an error: {response.status_code}'))
            response.raise_for_status()

    def handle(self, *args, **kwargs):
        source = str(kwargs['source'])
        if os.path.isfile(source):
            with open(source, 'r') as file:
                list_of_links = file.readlines()
            for link in list_of_links:
                self.fill_data_from_link(link)

        else:
            self.fill_data_from_link(source)

