from rest_framework import generics as api_views, permissions
from rest_framework.pagination import LimitOffsetPagination

from social_api.posts.models import Post
from social_api.posts.serializers import CommonPostSerializer


# Предложеният код използва LimitOffsetPagination, който позволява на клиентите да задават "offset" (отместване)
# и "limit" (ограничение) за резултатите, които искат да видят. Този вид пагинация обаче е по-подходящ за
# "infinite scroll", тъй като не изисква клиентите да проследяват номера на страниците
# и е по-удобен за скролиране в нататъшните резултати.


class FeedListAPIView(api_views.ListAPIView):
    queryset = Post.objects \
        .filter(status='Published') \
        .order_by('-timestamps')
    serializer_class = CommonPostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
