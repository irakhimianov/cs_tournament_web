from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

import core.models
import league.models


class Profile(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(label='Администратор')

    class Meta:
        model = core.models.Profile
        fields = '__all__'

    @extend_schema_field(bool)
    def get_is_admin(self, instance: core.models.Profile) -> bool:
        return instance.user.is_superuser or instance.user.is_staff


class Tournament(serializers.ModelSerializer):
    is_finished = serializers.SerializerMethodField(label='Завершен')

    class Meta:
        model = league.models.Tournament
        fields = '__all__'

    @extend_schema_field(bool)
    def get_is_finished(self, instance: league.models.Tournament) -> bool:
        return bool(instance.finished_at)


class Team(serializers.ModelSerializer):
    class Meta:
        model = league.models.Team
        fields = '__all__'


class Player(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField(label='Команды')
    is_agreed = serializers.SerializerMethodField(label='Принял правила')
    is_questioned = serializers.SerializerMethodField(label='Прошел анкету')
    is_verified = serializers.SerializerMethodField(label='Проверен')
    with_team = serializers.SerializerMethodField(label='С командой')

    class Meta:
        model = league.models.Player
        fields = '__all__'

    @extend_schema_field(Team(many=True))
    def get_teams(self, instance: league.models.Player) -> list[dict]:
        if not instance.teams.exists():
            return []

        qs = league.models.Team.objects.filter(players__player=instance)
        return Team(instance=qs, many=True).data

    @extend_schema_field(bool)
    def get_is_agreed(self, instance: league.models.Player) -> bool:
        return bool(instance.agreed_at)

    @extend_schema_field(bool)
    def get_is_questioned(self, instance: league.models.Player) -> bool:
        return bool(instance.questioned_at)

    @extend_schema_field(bool)
    def get_is_verified(self, instance: league.models.Player) -> bool:
        return bool(instance.verified_at)

    @extend_schema_field(bool)
    def get_with_team(self, instance: league.models.Player) -> bool:
        return instance.teams.exists()


class PlayerCreate(serializers.ModelSerializer):
    class Meta:
        model = league.models.Player
        fields = (
            'telegram_id',
            'telegram_username',
            'name',
            'contact',
            'sphere_work',
            'vertical_work',
            'steam_url',
            'faceit_url',
            'faceit_level',
            'agreed_at',
            'verified_at',
        )


class PlayerEdit(serializers.ModelSerializer):
    class Meta:
        model = league.models.Player
        fields = (
            'name',
            'contact',
            'sphere_work',
            'vertical_work',
            'steam_url',
            'faceit_url',
            'faceit_level',
            'agreed_at',
            'verified_at',
        )


class TeamCreate(serializers.ModelSerializer):
    default_error_messages = {
        'created_by': 'Профиль игрока не прошел проверку администратором',
    }

    class Meta:
        model = league.models.Team
        fields = ('name', 'created_by')


class TeamEdit(serializers.ModelSerializer):
    class Meta:
        model = league.models.Team
        fields = ('name',)


class TeamPlayer(serializers.ModelSerializer):
    team = Team(label='Команда')
    player = Player(label='Игрок')

    class Meta:
        model = league.models.TeamPlayer
        fields = '__all__'


class TeamPlayerCreate(serializers.Serializer):
    player = serializers.PrimaryKeyRelatedField(label='Игрок', queryset=league.models.Player.objects.all())


class TournamentPlayer(serializers.ModelSerializer):
    class Meta:
        model = league.models.TournamentPlayer
        fields = '__all__'
