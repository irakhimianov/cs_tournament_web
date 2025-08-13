import factory
import faker

fake_ru = faker.Faker('ru_RU')


class User(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda _: fake_ru.user_name())
    last_name = factory.Sequence(lambda _: fake_ru.last_name_male())
    first_name = factory.Sequence(lambda _: fake_ru.first_name_male())
    email = factory.Sequence(lambda _: fake_ru.email())
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = factory.Sequence(lambda _: fake_ru.pybool())

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)


class Profile(factory.django.DjangoModelFactory):
    user = factory.SubFactory('core.factories.User')
    telegram_id = factory.Sequence(lambda _: str(fake_ru.random_int(min=10_000_000, max=99_999_999)))
    telegram_username = factory.Sequence(lambda _: fake_ru.user_name())

    class Meta:
        model = 'core.Profile'
        django_get_or_create = ('user',)
