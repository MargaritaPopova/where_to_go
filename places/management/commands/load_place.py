from json.decoder import JSONDecodeError
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from requests import RequestException
from places.models import Location, Image


class Command(BaseCommand):
    """
    command: python manage.py load_place <link_to_json_file>
    Команда для заполнения данными локации на карте. Принимает аргументом ссылку на json-файл с описанием локации.
    Если файл содержит данные в неверном формате, ссылка игнорируется
    """
    help = 'Load location info from a link to json file'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, *args, **kwargs):
        link = str(kwargs['link'])
        try:
            location_dict = requests.get(link).json()
            location, created = Location.objects.get_or_create(
                title=location_dict['title'],
                defaults={
                    'lng': location_dict['coordinates']['lng'],
                    'lat': location_dict['coordinates']['lat'],
                    'long_description': location_dict['description_long'],
                    'short_description': location_dict['description_short'],
                    'properties_title': location_dict['title']}
            )
            if created:
                for img in location_dict['imgs']:
                    img_file = ContentFile(requests.get(img).content)
                    filename = img.split('/')[-1]
                    loc_img, created = Image.objects.get_or_create(
                        location_id=location.id,
                        image=filename
                    )
                    if created:
                        loc_img.image.save(filename, img_file, save=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully read file {link} \n'
                                                     f'Created Location object: {location.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Location {location.title} already exists, defaults updated.'))
        except (JSONDecodeError, RequestException):
            self.stdout.write(
                self.style.ERROR(f'Link {link} is incorrect or contains wrong input format, ignored.'))
