from django_filters import rest_framework as filters
from django.db.models import Q, QuerySet

import core.models
import league.models


class Profile(filters.FilterSet):
    telegram_id = filters.CharFilter(label='ID в telegram', lookup_expr='iexact')
    telegram_username = filters.CharFilter(label='Имя пользователя в telegram', lookup_expr='istartswith')
    is_admin = filters.BooleanFilter(label='Администратор', method='filter_is_admin')

    class Meta:
        model = core.models.Profile
        fields = ('telegram_id', 'telegram_username', 'is_admin')

    def filter_is_admin(
            self,
            qs: QuerySet[core.models.Profile],
            name: str,
            value: bool,
    ) -> QuerySet[core.models.Profile]:
        return qs.filter(Q(user__is_superuser=value) | Q(user__is_staff=value)).distinct()


class Tournament(filters.FilterSet):
    name = filters.CharFilter(label='Наименование', lookup_expr='istartswith')
    is_finished = filters.BooleanFilter(label='Завершен', method='filter_is_finished')

    class Meta:
        model = league.models.Tournament
        fields = ('name', 'is_finished')

    def filter_is_finished(
            self,
            qs: QuerySet[league.models.Tournament],
            name: str,
            value: bool,
    ) -> QuerySet[league.models.Tournament]:
        return qs.exclude(finished_at__isnull=value)


class Player(filters.FilterSet):
    telegram_id = filters.CharFilter(label='ID в telegram', lookup_expr='iexact')
    telegram_username = filters.CharFilter(label='Имя пользователя в telegram', lookup_expr='istartswith')
    is_agreed = filters.BooleanFilter(label='Принял правила', method='filter_is_agreed')
    is_questioned = filters.BooleanFilter(label='Прошел анкету', method='filter_is_questioned')
    is_verified = filters.BooleanFilter(label='Проверен администратором', method='filter_is_verified')
    with_team = filters.BooleanFilter(label='С командой', method='filter_with_team')
    team = filters.ModelChoiceFilter(
        label='Команда',
        queryset=league.models.Team.objects.all(),
        method='filter_team',
    )

    class Meta:
        model = league.models.Player
        fields = ('telegram_id', 'telegram_username', 'is_agreed', 'is_questioned', 'is_verified', 'with_team', 'team')

    def filter_is_agreed(
            self,
            qs: QuerySet[league.models.Player],
            name: str,
            value: bool,
    ) -> QuerySet[league.models.Player]:
        return qs.exclude(agreed_at__isnull=value)

    def filter_is_questioned(
            self,
            qs: QuerySet[league.models.Player],
            name: str,
            value: bool,
    ) -> QuerySet[league.models.Player]:
        return qs.exclude(questioned_at__isnull=value)

    def filter_is_verified(
            self,
            qs: QuerySet[league.models.Player],
            name: str,
            value: bool,
    ) -> QuerySet[league.models.Player]:
        return qs.exclude(verified_at__isnull=value)

    def filter_with_team(
            self,
            qs: QuerySet[league.models.Player],
            name: str,
            value: bool,
    ) -> QuerySet[league.models.Player]:
        return qs.exclude(teams__isnull=value)

    def filter_team(
            self,
            qs: QuerySet[league.models.Player],
            name: str,
            value: league.models.Team,
    ) -> QuerySet[league.models.Player]:
        return qs.filter(teams__team=value)


class Team(filters.FilterSet):
    name = filters.CharFilter(label='Наименование', lookup_expr='istartswith')
    invite_code = filters.CharFilter(label='Пригласительный код', lookup_expr='iexact')

    class Meta:
        model = league.models.Team
        fields = ('name', 'invite_code')


class TournamentPlayer(filters.FilterSet):
    class Meta:
        model = league.models.TournamentPlayer
        fields = ('tournament', 'player')
