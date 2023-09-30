from cloudinary.uploader import upload
from django.contrib.auth import authenticate
from rest_framework import serializers

from social_api.users.models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'description', 'profile_picture')

    def validate_profile_picture(self, value):
        # Upload the profile picture to Cloudinary
        if value:
            result = upload(value)
            return result['secure_url']
        return None


# Used for validation of the data and for authentication
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials')
        else:
            raise serializers.ValidationError('Need both "email" and password')

        data['user'] = user
        return data
