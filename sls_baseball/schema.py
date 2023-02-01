import strawberry
from typing import List
from baseball import models
from .types import Player, League, PlayerAttribute
from .inputs import PlayerInput, LeagueInput
from strawberry_django import mutations

@strawberry.type
class Query:
    players: List[Player] = strawberry.django.field()

@strawberry.type
class Mutation:
    createLeague: League = mutations.create(LeagueInput)
    @strawberry.mutation
    def createPlayer(self, info, input: PlayerInput) -> Player:
        player = models.Player.objects.create(first_name=input.first_name, last_name=input.last_name)
        attribute = models.PlayerAttribute.objects.create(
            player=player,
            composure=input.attributes.composure,
            endurance=input.attributes.endurance,
            intellect=input.attributes.intellect,
            reflexes=input.attributes.reflexes,
            speed=input.attributes.speed,
            strength=input.attributes.strength,
            willpower=input.attributes.willpower,
        )
        return player
    
    # @strawberry.mutation
    # def createPlayers(self, info, input: List[PlayerInput]) -> List[Player]:


schema = strawberry.Schema(query=Query, mutation=Mutation)