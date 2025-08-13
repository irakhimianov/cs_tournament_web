from typing import Type

from rest_framework import status
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.views.decorators.cache import cache_page

import core.models
import league.models
from api.v1 import filters, serializers


class Profile(ReadOnlyModelViewSet):
    queryset = core.models.Profile.objects.select_related('user').all()
    serializer_class = serializers.Profile
    filterset_class = filters.Profile

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class Tournament(ReadOnlyModelViewSet):
    queryset = league.models.Tournament.objects.all()
    serializer_class = serializers.Tournament
    filterset_class = filters.Tournament

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class Player(ModelViewSet):
    queryset = league.models.Player.objects.prefetch_related('teams').all()
    filterset_class = filters.Player

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ('retrieve', 'list'):
            return serializers.Player
        if self.action in ('update', 'partial_update'):
            return serializers.PlayerEdit
        return serializers.PlayerCreate


class Team(ModelViewSet):
    queryset = league.models.Team.objects.select_related('created_by').all()
    filterset_class = filters.Team

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ('retrieve', 'list'):
            return serializers.Team
        if self.action in ('update', 'partial_update'):
            return serializers.TeamEdit
        return serializers.TeamCreate

    @extend_schema(
        request=serializers.TeamPlayerCreate,
        responses={201: serializers.TeamPlayer},
    )
    @action(methods=['POST'], detail=True, serializer_class=serializers.TeamPlayerCreate, url_path='players')
    def add_player(self, request: Request, *args, **kwargs) -> Response:
        serializer = serializers.TeamPlayerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = self.get_object()
        tp, _ = league.models.TeamPlayer.objects.get_or_create(team=team, **serializer.validated_data)
        serializer = serializers.TeamPlayer(instance=tp)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TournamentPlayer(ModelViewSet):
    queryset = league.models.TournamentPlayer.objects.all()
    serializer_class = serializers.TournamentPlayer
    filterset_class = filters.TournamentPlayer
