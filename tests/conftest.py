from typing import Iterator

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import core.factories

pytest_plugins = ['tests.fixtures']


@pytest.mark.django_db
@pytest.fixture
def superuser() -> User:
    """Фикстура с суперпользователем"""
    return core.factories.User(is_superuser=True)


@pytest.mark.django_db
@pytest.fixture
def api_client(superuser: User) -> Iterator[APIClient]:
    """Фикстура API-клиента"""
    api_client = APIClient()
    token = personal_token(user=superuser)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    yield api_client
    api_client.force_authenticate(user=superuser)


@pytest.mark.django_db
def personal_token(user: User) -> Token:
    """Фикстура аутентификационного токена"""
    token, _ = Token.objects.get_or_create(user=user)
    return token
