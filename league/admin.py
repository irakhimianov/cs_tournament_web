from typing import Type

from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.utils import timezone

from league import models, services


class TeamPlayerInline(admin.TabularInline):
    model = models.TeamPlayer
    fields = ('player',)
    show_change_link = True
    extra = 0


@admin.register(models.Tournament)
class Tournament(admin.ModelAdmin):
    list_display = ('name', 'is_finished')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(boolean=True, ordering='finished_at', description='завершен')
    def is_finished(self, instance: models.Tournament) -> bool:
        return bool(instance.finished_at)


@admin.register(models.Player)
class Player(admin.ModelAdmin):
    list_display = ('__str__', 'is_verified')
    search_fields = ('telegram_id', 'telegram_username', 'name')
    readonly_fields = ('created_at', 'updated_at')
    actions = ('verify',)

    @admin.display(boolean=True, ordering='verified_at', description='проверен')
    def is_verified(self, instance: models.Player) -> bool:
        return bool(instance.verified_at)

    @admin.action(description='Отметить, что игроки прошли проверку')
    def verify(self, request: HttpRequest, qs: QuerySet[models.Player]) -> None:
        qs.update(verified_at=timezone.now())
        for player in qs:
            services.notify_player_verification(instance=player)


@admin.register(models.Team)
class Team(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name', 'created_by__telegram_id', 'created_by__telegram_username')
    readonly_fields = ('invite_code', 'created_at', 'updated_at')
    autocomplete_fields = ('created_by',)
    inlines = (TeamPlayerInline,)


@admin.register(models.TeamPlayer)
class TeamPlayer(admin.ModelAdmin):
    list_display = ('team', 'player')
    search_fields = ('team__name', 'player__telegram_id', 'player__telegram_username')
    list_filter = ('team',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('team', 'player')


@admin.register(models.TournamentPlayer)
class TournamentPlayer(admin.ModelAdmin):
    list_display = ('tournament', 'player', 'is_confirmed')
    search_fields = ('tournament__name', 'player__telegram_id', 'player__telegram_username')
    list_filter = ('tournament',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('tournament', 'player')

    @admin.display(boolean=True, ordering='confirmed_at', description='подтвердил')
    def is_confirmed(self, instance: models.TournamentPlayer) -> bool:
        return bool(instance.confirmed_at)
