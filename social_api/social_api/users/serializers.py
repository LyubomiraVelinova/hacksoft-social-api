from cloudinary.uploader import upload
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from social_api.posts.models import Like, Post
from social_api.users.models import CustomUser

UserModel = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'password')


# Used for validation of the data and for authentication
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Users are authenticated using email and password
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials')
            # until a Superuser marks that user as valid, the newly registered user cannot actually login.
            if not user.is_valid:
                raise serializers.ValidationError('User is not valid')
        else:
            raise serializers.ValidationError('Need both "email" and password')

        data['user'] = user
        return data


class ProfileUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'description', 'profile_picture')

    def update(self, instance, validated_data):
        # for field in self.Meta.fields:
        #     setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.description = validated_data.get('description', instance.description)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)

        if instance.profile_picture:
            # Upload the profile picture to Cloudinary and get the URL
            result = upload(instance.profile_picture)
            instance.profile_picture = result['secure_url']

        instance.save()
        return instance


class ProfileUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'description',
            'profile_picture',
        )

    # Total likes is the sum of likes on all posts that are created by the logged-in user.
    @staticmethod
    def get_total_likes(obj):
        return Like.objects.filter(post__author=obj).count()

    # Total posts is the count of all posts that are created by the logged-in user.
    @staticmethod
    def get_total_posts(obj):
        return Post.objects.filter(author=obj).count()
