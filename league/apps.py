from django.apps import AppConfig


class LeagueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'league'
    verbose_name = 'лига'

    def ready(self) -> None:
        import league.signals  # noqa
