from django.db import models

class Pokemons(models.Model):
    pokeapi_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    base_experience = models.IntegerField() #The base experience gained for defeating this Pokémon
    height = models.IntegerField()
    is_default = models.BooleanField() #Set for exactly one Pokémon used as the default for each s# pecies.
    order = models.IntegerField() #Order for sorting. Almost national order, except families are grouped together.
    weight = models.IntegerField()
    location_area_encounters = models.URLField(null=True, blank=True)  # A link to a list of location areas, as well as encounter details pertaining to specific versions.

    abilities = models.JSONField(null=True, blank=True)
    forms = models.JSONField(null=True, blank=True)
    held_items = models.JSONField(null=True, blank=True)
    moves = models.JSONField(null=True, blank=True)
    past_types = models.JSONField(null=True, blank=True)
    past_abilities = models.JSONField(null=True, blank=True)
    sprites = models.JSONField(null=True, blank=True)
    cries = models.JSONField(null=True, blank=True)
    species = models.JSONField(null=True, blank=True)
    stats = models.JSONField(null=True, blank=True)
    types = models.JSONField(null=True, blank=True)

class EvolutionChain(models.Model):
    is_baby = models.BooleanField()
    pok_species = models.JSONField(null=True, blank=True)
    species = models.JSONField(null=True, blank=True)
    evolution_details = models.JSONField(null=True, blank=True)
    evolves_to = models.JSONField(null=True, blank=True)
    pokemon = models.OneToOneField('Pokemons', on_delete=models.CASCADE, related_name='evolution_chain')



