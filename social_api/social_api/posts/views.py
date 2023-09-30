from rest_framework import generics as api_views, status
from rest_framework import permissions
from rest_framework.response import Response

from social_api.posts.models import Post
from social_api.posts.serializers import CommonPostSerializer


# Submit a new post
class PostCreateAPIView(api_views.CreateAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        status = self.request.data.get('status', 'Draft')
        serializer.save(author=self.request.user, status=status)


# Like a post
class PostLikeAPIView(api_views.CreateAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        post.likes.add(self.request.user)
        post.save()


# Unlike a post
class PostUnlikeAPIView(api_views.DestroyAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.likes.remove(self.request.user)


class PostSoftDeleteAPIView(api_views.DestroyAPIView):
    # Когато извиквате self.get_object() в изгледа, той използва queryset и информацията от URL параметрите, за да намери конкретния пост, който трябва да бъде "soft" изтрит.
    queryset = Post.objects.all()
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark post as 'soft deleted'
        instance.is_deleted = True
        instance.save()
        return Response({'message': 'Post is soft deleted'}, status=status.HTTP_204_NO_CONTENT)
