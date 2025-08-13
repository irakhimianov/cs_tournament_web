from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1 import views

app_name = 'v1'
router = DefaultRouter()

router.register('profiles', views.Profile, 'profiles')
router.register('tournaments', views.Tournament, 'tournaments')
router.register('players', views.Player, 'players')
router.register('teams', views.Team, 'teams')
router.register('tournament_players', views.TournamentPlayer, 'tournament_players')


urlpatterns = [
    path('', include(router.urls)),
]
