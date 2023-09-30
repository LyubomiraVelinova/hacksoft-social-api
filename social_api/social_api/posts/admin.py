from django.contrib import admin

from social_api.posts.models import Post, Like


@admin.action(description='Restore selected deleted post')
def restore_posts(self, request, queryset):
    queryset.update(is_deleted=False)
    self.message_user(request, f'Successfully restored {queryset.id} post.')


# I can add this field status

# @staticmethod
# def mark_as_published(self, request, queryset):
#     queryset.update(status='published')
#
# @staticmethod
# def mark_as_draft(self, request, queryset):
#     queryset.update(status='draft')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'timestamps', 'is_deleted', 'status']
    list_filter = ['author', 'timestamps', 'is_deleted']
    actions = [restore_posts]
    # 'mark_as_published', 'mark_as_draft'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
