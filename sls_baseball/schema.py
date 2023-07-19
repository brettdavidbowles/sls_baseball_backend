import strawberry
from typing import List
from baseball import models
from .types import Player, League, PlayerAttribute, Game, User, Team, Lineup, GameFilter, UserGame
from .inputs import PlayerInput, LeagueInput, UserInput, TeamInput, LineupPlayerInput
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


def get_game_by_id(id: str):
    return models.Game.objects.get(id=id)


def get_games_by_user(info):
    request: HttpRequest = info.context.request
    if not request.user.is_authenticated:
        return []
    home_games = models.Game.objects.filter(
        home_team__managers__user=request.user)
    away_games = models.Game.objects.filter(
        away_team__managers__user=request.user)
    user_teams = models.Team.objects.filter(managers__user=request.user)
    user_games = (home_games | away_games).order_by("-date_time")
    games = [
        UserGame(
            id=game.id,
            date_time=game.date_time,
            home_team=game.home_team,
            away_team=game.away_team,
            league=game.league,
            season=game.season,
            is_past=game.is_past,
            lineup_id=next(
                (lineup.id for lineup in game.lineups.all() if lineup.team in user_teams), None)
        ) for game in user_games]
    return games


def get_lineup_by_id(id: str):
    return models.Lineup.objects.get(id=id)


def get_bench_by_lineup_id(id: str):
    lineup = models.Lineup.objects.get(id=id)
    team = lineup.team
    lineup_players_ids = models.LineupPlayer.objects.filter(
        lineup=lineup).values_list("player__id", flat=True)
    return team.players.exclude(id__in=lineup_players_ids)


def get_games():
    return models.Game.objects.all()


@strawberry.type
class Query:
    me: User = auth.current_user()
    auth: User = strawberry.django.field(resolver=get_current_user)
    players: List[Player] = strawberry.django.field()
    leagues: List[League] = strawberry.django.field()
    teams: List[Team] = strawberry.django.field()
    games: List[Game] = strawberry.django.field(
        resolver=get_games
    )
    gameById: Game = strawberry.django.field(
        pagination=False,
        resolver=get_game_by_id
    )
    teamsByUser: List[Team] = strawberry.django.field(
        resolver=get_team_by_user)
    teamById: Team = strawberry.django.field(
        resolver=get_team_by_id)
    playerById: Player = strawberry.django.field(
        resolver=get_player_by_id)
    lineupById: Lineup = strawberry.django.field(
        resolver=get_lineup_by_id)
    benchByLineupId: List[Player] = strawberry.django.field(
        resolver=get_bench_by_lineup_id)
    gamesByUser: List[UserGame] = strawberry.django.field(
        resolver=get_games_by_user)


@strawberry.type
class Mutation:
    logout = auth.logout()
    register: User = auth.register(UserInput)
    createLeague: League = mutations.create(LeagueInput)

    @strawberry.mutation
    def register(self, info, input: UserInput) -> User:
        user = models.User.objects.create_user(
            username=input.username.lower(), password=input.password, email=input.email)
        return user

    @strawberry.mutation
    def login(self, info, username: str, password: str) -> User:
        request: HttpRequest = info.context.request
        user = authenticate(
            request, username=username.lower(), password=password)
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

    @strawberry.mutation
    # this works but need a bunch of error handling
    def update_lineup(
        self,
        info,
        id: strawberry.ID,
        players: List[LineupPlayerInput]
    ) -> Lineup:
        request: HttpRequest = info.context.request
        lineup = models.Lineup.objects.get(id=id)
        if not request.user.is_authenticated:
            raise Exception('User is not authenticated')
        if not lineup.team.managers.filter(user=request.user).exists():
            raise Exception('User is not authorized to update this lineup')
        if lineup.game.is_past:
            raise Exception('Cannot update lineup for past game')
        lineup.players.all().delete()
        new_players = []
        for player in players:
            new_players.append(models.LineupPlayer(
                lineup=lineup,
                player=models.Player.objects.get(id=player.id),
                position=player.position,
                batting_order_number=player.batting_order_number
            ))
        models.LineupPlayer.objects.bulk_create(new_players)
        return lineup


schema = strawberry.Schema(query=Query, mutation=Mutation)
