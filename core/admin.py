from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import models as auth_models
from django.utils.translation import gettext_lazy as _

from core import models

admin.site.unregister(auth_models.User)
admin.site.unregister(auth_models.Group)


class ProfileInline(admin.TabularInline):
    model = models.Profile
    fk_name = 'user'
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(models.Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'telegram_username')
    search_fields = ('user__username', 'telegram_id', 'telegram_username')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('user',)


@admin.register(auth_models.User)
class User(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    filter_horizontal = ()
    inlines = (ProfileInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
