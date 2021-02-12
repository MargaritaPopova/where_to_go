import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Location, Image


class Command(BaseCommand):
    help = 'Load location info from a link to json file'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, *args, **kwargs):
        link = kwargs['link']
        location_dict = requests.get(link).json()
        location, created = Location.objects.get_or_create(
            title=location_dict['title'],
            lng=location_dict['coordinates']['lng'],
            lat=location_dict['coordinates']['lat'],
            description_long=location_dict['description_long'],
            description_short=location_dict['description_short'],
            properties_title=location_dict['title']
        )
        if created:
            for img in location_dict['imgs']:
                img_file = ContentFile(requests.get(img).content)
                filename = img.split('/')[-1]
                loc_img = Image.objects.create(location_id=location.id)
                loc_img.image.save(filename, img_file, save=True)

        self.stdout.write(self.style.SUCCESS(f'Successfully read file {link} \n'
                                             f'Created Location object'))
