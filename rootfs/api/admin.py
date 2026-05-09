from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from oauth2_provider.admin import ApplicationAdmin as BaseApplicationAdmin

from .models import User, Message, MessagePreference, Application


try:
    admin.site.unregister(Application)
except admin.sites.NotRegistered:
    pass


@admin.register(Application)
class ApplicationAdmin(BaseApplicationAdmin):
    list_display = (
        "id", "name", "user", "client_type",
        "authorization_grant_type", "allowed_scopes",
    )


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'title', 'severity', 'is_read', 'created_at')
    list_filter = ('category', 'severity', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


class MessagePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_alerts', 'push_alerts')
    search_fields = ('user__username',)


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessagePreference, MessagePreferenceAdmin)
