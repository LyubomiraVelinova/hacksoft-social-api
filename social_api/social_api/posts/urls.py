from django.urls import path, include

from social_api.posts.views import PostCreateAPIView, PostLikeAPIView, PostUnlikeAPIView, PostSoftDeleteAPIView, \
    PostSubmitAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='create post'),
    path('submit/', PostSubmitAPIView.as_view(), name='submit post'),
    path('<int:pk>/', include([
        path('like/', PostLikeAPIView.as_view(), name='like post'),
        path('unlike/', PostUnlikeAPIView.as_view(), name='unlike post'),
        path('delete/', PostSoftDeleteAPIView.as_view(), name='soft delete post'),
    ])),
]
