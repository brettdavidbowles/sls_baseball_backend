import strawberry
from baseball import models
from strawberry import auto
from django.contrib.auth import get_user_model

@strawberry.django.input(get_user_model())
class UserInput:
    username: auto
    email: auto
    password: auto

@strawberry.django.input(models.Player)
class PlayerInput:
    first_name: auto
    last_name: auto
    team: str
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

@strawberry.django.input(models.Team)
class TeamInput:
    name: auto
    league: str
    # user: str