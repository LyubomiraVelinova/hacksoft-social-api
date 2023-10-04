from rest_framework import serializers

from social_api.posts.models import Post


class CommonPostSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'
