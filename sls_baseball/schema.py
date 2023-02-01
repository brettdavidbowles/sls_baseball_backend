import strawberry
from typing import List
from .types import Player
from .inputs import PlayerInput
from strawberry_django import mutations

@strawberry.type
class Query:
    players: List[Player] = strawberry.django.field()

@strawberry.type
class Mutation:
    createPlayers: List[Player] = mutations.create(PlayerInput)
    createPlayer: Player = mutations.create(PlayerInput)

schema = strawberry.Schema(query=Query, mutation=Mutation)