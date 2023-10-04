from django.contrib import admin

from social_api.posts.models import Post, Like

'''
Superusers can “restore” a post that is “soft” deleted.
'''


@admin.action(description='Restore selected deleted post')
def restore_posts(self, request, queryset):
    queryset.update(is_deleted=False)
    self.message_user(request, f'Successfully restored {queryset.id} post.')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'timestamps', 'status']
    list_filter = ['author', 'timestamps', 'status']
    actions = [restore_posts]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
