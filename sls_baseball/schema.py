import strawberry
from typing import List
from baseball import models
from .types import Player, League, PlayerAttribute
from .inputs import PlayerInput, LeagueInput
from strawberry_django import mutations
from itertools import islice

@strawberry.type
class Query:
    players: List[Player] = strawberry.django.field()
    leagues: List[League] = strawberry.django.field()

@strawberry.type
class Mutation:
    createLeague: League = mutations.create(LeagueInput)
    @strawberry.mutation
    def createPlayer(self, info, input: PlayerInput) -> Player:
        player = models.Player.objects.create(first_name=input.first_name, last_name=input.last_name, team=models.Team.objects.get(name=input.team))
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
    
    @strawberry.mutation
    def createPlayers(self, info, input: List[PlayerInput]) -> List[Player]:
        batch_size = 500
        players = [models.Player(first_name=player.first_name, last_name=player.last_name, team=models.Team.objects.get(name=player.team)) for player in input]
        full_length = len(players)
        players_list = list(players)
        attributes = [models.PlayerAttribute(
            player=players_list[index],
            composure=player.attributes.composure,
            endurance=player.attributes.endurance,
            intellect=player.attributes.intellect,
            reflexes=player.attributes.reflexes,
            speed=player.attributes.speed,
            strength=player.attributes.strength,
            willpower=player.attributes.willpower,
        ) for index, player in enumerate(input)]

        number_created = 0
        while number_created < full_length:
            players_batch = list(islice(players, number_created, number_created + batch_size))
            attributes_batch = list(islice(attributes, number_created, number_created + batch_size))
            if not players_batch:
                break
            models.Player.objects.bulk_create(players_batch, batch_size)
            models.PlayerAttribute.objects.bulk_create(attributes_batch, batch_size)
            number_created += batch_size
        return players

schema = strawberry.Schema(query=Query, mutation=Mutation)