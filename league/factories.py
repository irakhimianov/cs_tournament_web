import factory
from faker import Faker

fake_ru = Faker('ru_RU')


class Tournament(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda _: fake_ru.word())

    class Meta:
        model = 'league.Tournament'
        django_get_or_create = ('name',)


class Player(factory.django.DjangoModelFactory):
    telegram_id = factory.Sequence(lambda _: str(fake_ru.random_int(min=10_000_000, max=99_999_999)))
    telegram_username = factory.Sequence(lambda _: fake_ru.user_name())
    contact = factory.Sequence(lambda _: fake_ru.phone_number())
    sphere_work = factory.Sequence(lambda _: fake_ru.job())
    vertical_work = factory.Sequence(lambda _: fake_ru.catch_phrase())
    steam_url = factory.LazyAttribute(lambda _: f'https://steamcommunity.com/id/{fake_ru.user_name()}')
    faceit_url = factory.LazyAttribute(lambda _: f'https://www.faceit.com/en/players/{fake_ru.user_name()}')
    faceit_level = factory.Sequence(lambda _: str(fake_ru.random_int(min=1, max=10)))

    class Meta:
        model = 'league.Player'


class Team(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda _: fake_ru.word())
    created_by = factory.SubFactory('league.factories.Player')

    class Meta:
        model = 'league.Team'
        django_get_or_create = ('name',)


class TeamPlayer(factory.django.DjangoModelFactory):
    team = factory.SubFactory('league.factories.Team')
    player = factory.SubFactory('league.factories.Player')

    class Meta:
        model = 'league.TeamPlayer'
        django_get_or_create = ('team', 'player')


class TournamentPlayer(factory.django.DjangoModelFactory):
    tournament = factory.SubFactory('league.factories.Tournament')
    player = factory.SubFactory('league.factories.Player')

    class Meta:
        model = 'league.TournamentPlayer'
        django_get_or_create = ('tournament', 'player')
