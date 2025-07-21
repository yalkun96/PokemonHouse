from rest_framework import serializers
from .models import *

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemons
        fields = '__all__'

class EvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolutionChain
        fields = '__all__'

