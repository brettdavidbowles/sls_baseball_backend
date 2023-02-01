import strawberry
from baseball import models
from strawberry import auto

@strawberry.django.input(models.Player)
class PlayerInput:
    first_name: auto
    last_name: auto
    attributes: 'PlayerAttributeInput'

@strawberry.django.input(models.PlayerAttribute)
class PlayerAttributeInput:
    composure: auto
    endurance: auto
    intellect: auto
    reflexes: auto
    speed: auto
    strength: auto
    willpower: auto