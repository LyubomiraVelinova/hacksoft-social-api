from rest_framework import generics as api_views, permissions
from rest_framework.pagination import LimitOffsetPagination

from social_api.posts.models import Post
from social_api.posts.serializers import CommonPostSerializer


'''
API that returns a feed of all posts that were published.
This API is going to be rendered in a list with “infinite scroll”.
The API is returning the last 20 posts.
Accessible for authenticated users only.
'''


class FeedListAPIView(api_views.ListAPIView):
    queryset = Post.objects \
        .filter(status='Published') \
        .order_by('-timestamps')
    serializer_class = CommonPostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
