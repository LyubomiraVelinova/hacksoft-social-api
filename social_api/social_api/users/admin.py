from django.contrib import admin

from social_api.users.models import CustomUser


# WHY STILL HAVE THE FIELD "username" IN DJANGO ADMIN PANEL???
@admin.action(description='Mark selected users as valid')
def mark_as_valid(self, request, queryset):
    queryset.update(is_sandboxed=False, is_valid=True)
    self.message_user(request, f'Successfully marked {queryset.count()} as valid.')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_sandboxed', 'date_joined', 'is_valid', 'is_superuser')
    list_filter = ('is_sandboxed', 'date_joined')
    actions = [mark_as_valid]
