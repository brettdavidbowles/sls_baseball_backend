import strawberry
from typing import List
from baseball import models
from .types import Player, League, PlayerAttribute, Game, User, Team
from .inputs import PlayerInput, LeagueInput, UserInput, TeamInput
from strawberry_django import auth, mutations
from itertools import islice
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login


def get_team_by_user(info):
    request: HttpRequest = info.context.request
    if not request.user.is_authenticated:
        return []
    return models.Team.objects.filter(managers__user=request.user)


def get_current_user(info):
    request: HttpRequest = info.context.request
    if not request.user.is_authenticated:
        return User(id="", username="", email="", managers=[])
    return request.user


def get_team_by_id(id: str):
    return models.Team.objects.get(id=id)


def get_player_by_id(id: str):
    return models.Player.objects.get(id=id)


@strawberry.type
class Query:
    me: User = auth.current_user()
    auth: User = strawberry.django.field(resolver=get_current_user)
    players: List[Player] = strawberry.django.field()
    leagues: List[League] = strawberry.django.field()
    games: List[Game] = strawberry.django.field()
    gameByPk: Game = strawberry.django.field(pagination=False)
    teamsByUser: List[Team] = strawberry.django.field(
        resolver=get_team_by_user)
    teamById: Team = strawberry.django.field(
        resolver=get_team_by_id)
    playerById: Player = strawberry.django.field(
        resolver=get_player_by_id)


@strawberry.type
class Mutation:
    logout = auth.logout()
    register: User = auth.register(UserInput)
    createLeague: League = mutations.create(LeagueInput)

    @strawberry.mutation
    def login(self, info, username: str, password: str) -> User:
        request: HttpRequest = info.context.request
        user = authenticate(
            request, username=username, password=password)
        if user is not None:
            login(request, user)
            return user
        else:
            return User(id="", username="", email="")

    @strawberry.mutation
    def createPlayer(self, info, input: PlayerInput) -> Player:
        player = models.Player.objects.create(
            first_name=input.first_name, last_name=input.last_name, team=models.Team.objects.get(name=input.team))
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
        players = [models.Player(first_name=player.first_name, last_name=player.last_name,
                                 team=models.Team.objects.get(name=player.team)) for player in input]
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
            players_batch = list(
                islice(players, number_created, number_created + batch_size))
            attributes_batch = list(
                islice(attributes, number_created, number_created + batch_size))
            if not players_batch:
                break
            models.Player.objects.bulk_create(players_batch, batch_size)
            models.PlayerAttribute.objects.bulk_create(
                attributes_batch, batch_size)
            number_created += batch_size
        return players

    @strawberry.mutation
    def createTeam(self, info, input: TeamInput) -> Team:
        request: HttpRequest = info.context.request
        if not request.user.is_authenticated:
            raise Exception('User is not authenticated')
        team = models.Team.objects.create(
            name=input.name, league=models.League.objects.get(name=input.league))
        models.Manager.objects.create(team=team, user=request.user)
        return team


schema = strawberry.Schema(query=Query, mutation=Mutation)
