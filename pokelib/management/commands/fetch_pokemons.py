import requests
from django.core.management.base import BaseCommand
from pokelib.models import Pokemons


class Command(BaseCommand):
    help = 'Fetch and save all pokemons from PokeAPI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            type=int,
            default=1,
            help='Starting Pokemon ID'
        )
    def handle(self, *args, **kwargs):
        url = 'https://pokeapi.co/api/v2/pokemon?limit=100000'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch pokemon list'))
            return

        pokemon_list = response.json()['results']

        for i, item in enumerate(pokemon_list, start=1):
            detail_url = item['url']
            detail_response = requests.get(detail_url)
            if detail_response.status_code != 200:
                continue

            data = detail_response.json()

            Pokemons.objects.update_or_create(
                pokeapi_id=data['id'],
                defaults={
                    'name': data['name'],
                    'base_experience': data['base_experience'],
                    'height': data['height'],
                    'is_default': data['is_default'],
                    'order': data['order'],
                    'weight': data['weight'],
                    'abilities': data['abilities'],
                    'forms': data['forms'],
                    'held_items': data['held_items'],
                    'moves': data['moves'],
                    'past_types': data['past_types'],
                    'past_abilities': data.get('past_abilities', []),
                    'sprites': data['sprites'],
                    'cries': data['cries'],
                    'species': data['species'],
                    'stats': data['stats'],
                    'types': data['types'],
                    'location_area_encounters': data.get('location_area_encounters'),
                }
            )

            self.stdout.write(f"Saved: {data['name']} ({i}/{len(pokemon_list)})")