from django.shortcuts import render
from rest_framework import generics as api_views, permissions
from rest_framework.pagination import PageNumberPagination

from social_api.posts.models import Post
from social_api.posts.serializers import PostSerializer


class CustomPagination(PageNumberPagination):
    page_size = 20


class FeedListAPIView(api_views.ListAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = (
        permissions.IsAuthenticated
    )
