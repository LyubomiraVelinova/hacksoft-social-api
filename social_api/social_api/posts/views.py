from rest_framework import generics as api_views, status
from rest_framework import permissions
from rest_framework.response import Response

from social_api.posts.models import Post, Like
from social_api.posts.serializers import PostSerializer, LikeSerializer


class PostListCreateView(api_views.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikeListCreateView(api_views.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class PostDeleteView(api_views.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark post as 'soft deleted'
        instance.is_deleted = True
        instance.save()
        return Response({'message': 'Post is soft deleted'}, status=status.HTTP_204_NO_CONTENT)
