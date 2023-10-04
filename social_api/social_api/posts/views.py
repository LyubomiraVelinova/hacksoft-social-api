from datetime import datetime

from rest_framework import generics as api_views
from rest_framework import views
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from social_api.posts.models import Post
from social_api.posts.serializers import CommonPostSerializer

'''
API for creating a new post. Post can be create just as a draft and it won`t be published.
Accessible for authenticated users only.
'''


class PostCreateAPIView(api_views.CreateAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # When creating a new post user can make a choice whether it is Draft or Published
    def create(self, request, *args, **kwargs):
        status = request.data.get('status', 'Draft')

        if status not in [choice[0] for choice in Post.STATUS_CHOICES]:
            return Response({'detail': 'Invalid status value. Status should be "Draft" or "Published".'},
                            status=status.HTTP_400_BAD_REQUEST)

        request.data['author'] = request.user.id
        request.data['status'] = status

        return super().create(request, *args, **kwargs)


'''
API for submitting a new post.
Accessible for authenticated users only.
'''


class PostSubmitAPIView(api_views.UpdateAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user != post.author:
            return Response({'detail': 'You do not have permission to change the status of this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Make the post 'Published' so that it can be submitted
        if post.status == 'Draft':
            post.status = 'Published'
            post.save()
            return Response({'message': 'Post submitted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'This post is already published.'}, status=status.HTTP_400_BAD_REQUEST)


'''
API for liking a post
Accessible for authenticated users only.
'''


class PostLikeAPIView(api_views.CreateAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        post.likes.add(self.request.user)
        post.save()


'''
API for disliking a post
Accessible for authenticated users only.
'''


class PostUnlikeAPIView(api_views.DestroyAPIView):
    serializer_class = CommonPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.likes.remove(self.request.user)


'''
API for deleting a post.
The post is “soft deleted”. This means - the post should stay in the database,
but it should not be returned in the feed.
'''


class PostSoftDeleteAPIView(views.APIView):
    @staticmethod
    def delete(request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Just mark the post as "soft_deleted" and not delete it from the db
        post.status = 'Deleted'
        post.deleted_at = datetime.now()
        post.save()

        return Response({'message': 'Post is soft deleted'}, status=status.HTTP_204_NO_CONTENT)
