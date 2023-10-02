from django.urls import path

from social_api.feed.views import FeedListAPIView

urlpatterns = [
    path('', FeedListAPIView.as_view(), name='published posts feed'),
]
