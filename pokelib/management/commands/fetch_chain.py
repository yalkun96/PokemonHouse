import requests
from django.core.management.base import BaseCommand
from pokelib.models import EvolutionChain, Pokemons


class Command(BaseCommand):
    help = 'Fetch and save evolution chains for all pokemons from PokeAPI'

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
                self.stdout.write(self.style.WARNING(f"Failed to fetch details for {item['name']}"))
                continue

            data = detail_response.json()


            species_url = data['species']['url']
            species_response = requests.get(species_url)
            if species_response.status_code != 200:
                self.stdout.write(self.style.WARNING(f"Failed to fetch species for {item['name']}"))
                continue

            species_data = species_response.json()
            evolution_chain_url = species_data['evolution_chain']['url']

            # get id from evolutionchain from URL
            chain_id = evolution_chain_url.rstrip('/').split('/')[-1]

            # Get data from evolutiochain
            chain_response = requests.get(evolution_chain_url)
            if chain_response.status_code != 200:
                self.stdout.write(self.style.WARNING(f"Failed to fetch evolution chain for {item['name']}"))
                continue

            chain_data = chain_response.json()
            chain = chain_data.get('chain', {})

            try:
                pokemon_obj = Pokemons.objects.get(pokeapi_id=data['id'])
            except Pokemons.DoesNotExist:
                # if pokemon not found skip or create
                self.stdout.write(self.style.WARNING(f"Pokemon {data['name']} not found in DB, skipping"))
                continue

            #Save chain in database
            EvolutionChain.objects.update_or_create(
                id=chain_data['id'],
                defaults={
                    'is_baby': chain.get('is_baby', False),
                    'pok_species': chain.get('species', {}),
                    'evolution_details': chain.get('evolution_details', []),
                    'evolves_to': chain.get('evolves_to', []),
                    'pokemon': pokemon_obj,
                }
            )

            self.stdout.write(f"Saved evolution chain for: {data['name']} ({i}/{len(pokemon_list)})")