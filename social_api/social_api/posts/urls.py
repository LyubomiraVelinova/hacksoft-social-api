from django.urls import path

from social_api.posts.views import PostCreateAPIView, PostLikeAPIView, PostUnlikeAPIView, PostSoftDeleteAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='create post'),
    path('like/', PostLikeAPIView.as_view(), name='like post'),
    path('unlike/', PostUnlikeAPIView.as_view(), name='unlike post'),
    path('delete/', PostSoftDeleteAPIView.as_view(), name='soft delete post'),
]
