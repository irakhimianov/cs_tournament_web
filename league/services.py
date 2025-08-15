import random
from typing import Optional

import requests
from django.conf import settings
from django.db import transaction

from league import models, tasks


def generate_invite_code(length: int = 6) -> str:
    """Генерация уникального цифрового кода заданной длины"""
    assert length > 0, 'Длина кода должна быть минимум 1 символ'

    start = 10 ** (length - 1)
    end = (10 ** length) - 1

    code = str(random.randint(start, end))
    return code


def notify_player_verification(instance: models.Player, old_instance: Optional[models.Player] = None) -> None:
    if instance.verified_at and (not old_instance or old_instance.verified_at is None):
        text = 'Ваша заявка одобрена!'
        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Меню', 'callback_data': 'menu'}],
            ],
        }
        return transaction.on_commit(lambda: tasks.send_telegram_message.delay(instance.pk, text, reply_markup))

    if instance.verified_at is None and (not old_instance or old_instance.verified_at):
        text = 'Ваша заявка отозвана!'
        return transaction.on_commit(lambda: tasks.send_telegram_message.delay(instance.pk, text))


class TelegramHandler:
    url = 'https://api.telegram.org/bot{token}/{method}'

    def __init__(self, token: str = settings.BOT_TOKEN) -> None:
        self.token = token

    def send_message(self, chat_id: int, text: str, reply_markup: Optional[dict] = None) -> requests.Response:
        url = self.url.format(token=self.token, method='sendMessage')
        payload = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            payload |= {'reply_markup': reply_markup}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response
