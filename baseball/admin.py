from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Player, PlayerAttribute, Team, League, Manager, Season, Game, Lineup, LineupPlayer, AtBat, LeftOnRunner, ScheduledGame


admin.site.register(User, UserAdmin)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(League)
admin.site.register(Manager)
admin.site.register(Season)
admin.site.register(Game)
admin.site.register(Lineup)
admin.site.register(LineupPlayer)
admin.site.register(AtBat)
admin.site.register(LeftOnRunner)
admin.site.register(ScheduledGame)
admin.site.register(PlayerAttribute)