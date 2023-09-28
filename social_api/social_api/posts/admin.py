from django.contrib import admin

from social_api.posts.models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'timestamps', 'is_deleted']
    list_filter = ['author', 'timestamps', 'is_deleted']
    actions = ['restore_deleted_posts']
    # 'mark_as_published', 'mark_as_draft'

    @staticmethod
    def restore_deleted_posts(self, request, queryset):
        queryset.update(is_deleted=False)

    # I can add this field status

    # @staticmethod
    # def mark_as_published(self, request, queryset):
    #     queryset.update(status='published')
    #
    # @staticmethod
    # def mark_as_draft(self, request, queryset):
    #     queryset.update(status='draft')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
