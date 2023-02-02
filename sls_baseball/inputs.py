import strawberry
from baseball import models
from strawberry import auto

@strawberry.django.input(models.Player)
class PlayerInput:
    first_name: auto
    last_name: auto
    # team: auto
    attributes: 'PlayerAttributeInput'

@strawberry.django.input(models.PlayerAttribute, partial=True)
class PlayerAttributeInput:
    composure: auto
    endurance: auto
    intellect: auto
    reflexes: auto
    speed: auto
    strength: auto
    willpower: auto

@strawberry.django.input(models.League)
class LeagueInput:
    name: auto