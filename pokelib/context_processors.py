from .models import Pokemons

def pokemon_types(request):
    types = set()
    for pokemon in Pokemons.objects.exclude(types__isnull=True):
        for type_data in pokemon.types:
            type_name = type_data.get('type', {}).get('name')
            if type_name:
                types.add(type_name.lower())
    return {'all_types': sorted(types)}