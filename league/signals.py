from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from league import models, services


@receiver(post_save, sender=models.Team)
def set_invite_code(sender: Type[models.Team], instance: models.Team, created: bool, **kwargs) -> None:
    """Присвоение invite_code после создания объекта"""
    if not created or instance.invite_code:
        return

    while True:
        code = services.generate_invite_code()
        if not models.Team.objects.filter(invite_code=code).exists():
            break

    instance.invite_code = code
    instance.save(update_fields=['invite_code'])


@receiver(post_save, sender=models.Team)
def set_team_creator(sender: Type[models.Team], instance: models.Team, created: bool, **kwargs) -> None:
    """После создания команды добавляем её создателя в `TeamPlayer`"""
    if created and instance.created_by:
        models.TeamPlayer.objects.get_or_create(team=instance, player=instance.created_by)
