from django.contrib import admin

from social_api.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_sandboxed')
    list_filter = ('is_sandboxed',)
