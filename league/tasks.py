from typing import Optional

import requests
from celery import shared_task

from league import models, services


@shared_task(
    autoretry_for=[requests.RequestException],
    retry_backoff=10,
    retry_kwargs={'max_retries': 5},
    acks_late=True,
)
def send_telegram_message(player_id: int, text: str, reply_markup: Optional[dict] = None) -> None:
    player = models.Player.objects.filter(id=player_id).first()

    if not player:
        return

    telegram_handler = services.TelegramHandler()
    telegram_handler.send_message(chat_id=player.telegram_id, text=text, reply_markup=reply_markup)
