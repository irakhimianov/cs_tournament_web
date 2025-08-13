from django.db import models


class DateTimeBase(models.Model):
    created_at = models.DateTimeField('когда создан', auto_now_add=True)
    updated_at = models.DateTimeField('когда обновлен', auto_now=True)

    class Meta:
        abstract = True


class Profile(DateTimeBase):
    user = models.OneToOneField(
        'auth.User',
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='profile',
    )
    telegram_id = models.CharField('ID в telegram', max_length=255, db_index=True)
    telegram_username = models.CharField('имя пользователя в telegram', max_length=255, blank=True)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        ordering = ('id',)

    def __str__(self) -> str:
        return str(self.user)
