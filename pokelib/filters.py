
from .models import Pokemons
from django_filters import FilterSet, CharFilter
from .models import Pokemons

from django_filters import FilterSet, CharFilter
from .models import Pokemons


class PokemonFilter(FilterSet):
    type = CharFilter(method='filter_by_type', label='Type')

    class Meta:
        model = Pokemons
        fields = ['name']  # Обычные поля для фильтрации

    def filter_by_type(self, queryset, name, value):

        if not value:
            return queryset

        filtered = [
            p for p in queryset
            if p.types and any(
                t.get('type', {}).get('name', '').lower() == value.lower()
                for t in p.types
            )
        ]
        pks = [p.pokeapi_id for p in filtered]
        return Pokemons.objects.filter(pokeapi_id__in=pks)