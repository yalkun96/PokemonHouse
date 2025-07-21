from django.urls import reverse
from rest_framework import generics
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework.views import APIView

from .filters import PokemonFilter
from .serializers import EvolutionSerializer, PokemonSerializer
import requests
from rest_framework.response import Response
from pokelib.models import EvolutionChain, Pokemons
import random
import json




#filter search
class PokemonList(ListView):
    model = Pokemons
    template_name = 'home.html'
    context_object_name = 'pokemons'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PokemonFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Теперь фильтрация будет работать

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset

        # Получаем уникальные типы для dropdown
        all_types = set()
        for pokemon in Pokemons.objects.exclude(types__isnull=True).only('types'):
            for type_data in pokemon.types or []:
                if type_data.get('type', {}).get('name'):
                    all_types.add(type_data['type']['name'].lower())

        context['all_types'] = sorted(all_types)
        return context



class PokemonAPI(APIView):
    def get(self, request, name_or_id):
        url = f'https://pokeapi.co/api/v2/pokemon/{name_or_id.lower()}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pokemon, created = Pokemons.objects.update_or_create(
                pokeapi_id=data['id'],
                defaults={
                    'name': data['name'],
                    'base_experience': data['base_experience'],
                    'height': data['height'],
                    'is_default': data['is_default'],
                    'order': data['order'],
                    'weight': data['weight'],
                    'location_area_encounters': data.get('location_area_encounters', None),

                    'abilities': data.get('abilities'),
                    'forms': data.get('forms'),
                    'held_items': data.get('held_items'),
                    'moves': data.get('moves'),
                    'past_types': data.get('past_types'),
                    'past_abilities': data.get('past_abilities'),
                    'sprites': data.get('sprites'),
                    'cries': data.get('cries'),
                    'species': data.get('species'),
                    'stats': data.get('stats'),
                    'types': data.get('types'),
                    'image': data['sprites']['front_default'],
                }
            )

            return Response({
                'message': 'Pokemon saved to database',
                'created': created,
                'pokemon_id': pokemon.pokeapi_id,
                'name': pokemon.name
            })

        return Response({"error": "Pokemon not found"}, status=404)



class EvolutionChainAPI(APIView):
    def get(self, request, chain_id):
        url = f'https://pokeapi.co/api/v2/evolution-chain/{chain_id}'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch evolution chain from PokeAPI"}, status=502)

        data = response.json()
        chain = data.get('chain')
        if not chain:
            return Response({"error": "No evolution chain data found"}, status=404)

        species_name = chain['species']['name']

        try:
            pokemon = Pokemons.objects.get(name=species_name)
        except Pokemons.DoesNotExist:
            return Response({"error": f"Pokemon '{species_name}' not found in DB"}, status=404)


        evolution_chain, created = EvolutionChain.objects.update_or_create(
            pokeapi_id=data['id'],
            defaults={
                'pokemon': pokemon,
                'is_baby': chain.get('is_baby', False),
                'species': chain.get('species'),
                'evolution_details': chain.get('evolution_details', []),
                'evolves_to': chain.get('evolves_to', []),
            }
        )

        return Response({"success": f"Evolution chain saved for {pokemon.name}"})



class PokemonInfo(DetailView):
    template_name = 'pokemon_info.html'
    model = Pokemons
    context_object_name = 'pokemon'
    pk_url_kwarg = 'pk'

class ChainInfo(DetailView):
    template_name = 'pokemon_info.html'  # отдельный шаблон для цепочки
    model = EvolutionChain
    context_object_name = 'chain'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chain_obj = context['chain']

        context['evolution_chain'] = chain_obj

        return context


#search
def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        pokemons = Pokemons.objects.filter(name__icontains=searched)
        return render(request, 'search_results.html', {
            'searched': searched,
            'pokemons': pokemons
        })
    return render(request, 'search_results.html', {})



