from django.contrib import admin
from .models import Player, PerformanceStat, Scout, Team, News, UpcomingMatch

# Register your models here.
admin.site.register(Player)
admin.site.register(PerformanceStat)
admin.site.register(Scout)
admin.site.register(Team)
admin.site.register(News)
admin.site.register(UpcomingMatch)