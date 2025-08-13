from django.db import models
from django.db.models.constraints import UniqueConstraint

import core.models


class Tournament(core.models.DateTimeBase):
    name = models.CharField('наименование', max_length=255, db_index=True)
    finished_at = models.DateTimeField('когда завершен', null=True, blank=True)

    class Meta:
        verbose_name = 'турнир'
        verbose_name_plural = 'турниры'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class Player(core.models.DateTimeBase):
    telegram_id = models.CharField('ID в telegram', max_length=255, db_index=True)
    name = models.CharField('имя', max_length=255, blank=True)
    telegram_username = models.CharField('имя пользователя в telegram', max_length=255, blank=True)
    contact = models.CharField(
        'контакт для связи',
        max_length=255,
        blank=True,
        help_text='Заполняется в случае отсутствия имени пользователя в telegram',
    )
    sphere_work = models.TextField('сфера', blank=True)
    vertical_work = models.TextField('вертикаль', blank=True)
    steam_url = models.TextField('ссылка на steam', blank=True)
    faceit_url = models.TextField('ссылка на faceit', blank=True)
    faceit_level = models.IntegerField('уровень faceit', default=0)
    agreed_at = models.DateTimeField('когда принял правила', null=True, blank=True)
    questioned_at = models.DateTimeField('когда прошел анкету', null=True, blank=True)
    verified_at = models.DateTimeField('когда прошел проверку администратором', null=True, blank=True)

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'
        ordering = ('id',)

    def __str__(self) -> str:
        if self.telegram_username:
            return f'{self.telegram_id} ({self.telegram_username})'
        return self.telegram_id


class Team(core.models.DateTimeBase):
    name = models.CharField('наименование', max_length=255, db_index=True)
    created_by = models.ForeignKey(
        'league.Player',
        verbose_name='создатель команды',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_teams',
    )
    invite_code = models.CharField(
        'пригласительный код',
        max_length=255,
        editable=False,
        blank=True,
        db_index=True,
        help_text='Уникальный код. Генерируется автоматически, для вступления игрока в команду по коду',
    )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class TeamPlayer(core.models.DateTimeBase):
    team = models.ForeignKey(
        'league.Team',
        verbose_name='команда',
        on_delete=models.CASCADE,
        related_name='players',
    )
    player = models.ForeignKey(
        'league.Player',
        verbose_name='игрок',
        on_delete=models.CASCADE,
        related_name='teams',
    )

    class Meta:
        verbose_name = 'игрок команды'
        verbose_name_plural = 'игроки команды'
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('team', 'player'), name='unique_team_player'),
        )

    def __str__(self) -> str:
        return f'{self.team}: {self.player}'


class TournamentPlayer(core.models.DateTimeBase):
    tournament = models.ForeignKey(
        'league.Tournament',
        verbose_name='турниры',
        on_delete=models.CASCADE,
        related_name='players',
    )
    player = models.ForeignKey(
        'league.Player',
        verbose_name='игрок',
        on_delete=models.CASCADE,
        related_name='tournaments',
    )
    confirmed_at = models.DateTimeField('когда подтвердил свое участие', null=True, blank=True)

    class Meta:
        verbose_name = 'участник турнира'
        verbose_name_plural = 'участники турнира'
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('tournament', 'player'), name='unique_tournament_player'),
        )

    def __str__(self) -> str:
        return f'{self.tournament}: {self.player}'
