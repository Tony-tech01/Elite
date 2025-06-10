from rest_framework import serializers
from .models import Player, Team, League, PerformanceStat, Scout, News, UpcomingMatch

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

class PerformanceStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceStat
        fields = '__all__'

class ScoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scout
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class UpcomingMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingMatch
        fields = '__all__'
