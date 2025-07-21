from django.urls import path

from pokelib.views import  PokemonAPI, EvolutionChainAPI, PokemonInfo, ChainInfo, search_venues, PokemonList

urlpatterns = [
    path('', PokemonList.as_view(), name='home'),
    #path('', HomePageView.as_view(), name='home'),
    path('api/pokemons/<str:name_or_id>/', PokemonAPI.as_view(), name='pokemon-api'),
    path('api/evolution', EvolutionChainAPI.as_view(), name='evolution-api'),
    path('pokemon/<int:pk>/', PokemonInfo.as_view(), name='pokemon-info'),
    path('chain/<int:pk>/', ChainInfo.as_view(), name='chain-info'),
    path('search/', search_venues, name='search_pokemon'),

]