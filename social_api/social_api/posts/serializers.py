from rest_framework import serializers

from social_api.posts.models import Post


class CommonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
