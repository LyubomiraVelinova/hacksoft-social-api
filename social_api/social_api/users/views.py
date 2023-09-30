from cloudinary.uploader import upload
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics as rest_views

from social_api.users.models import CustomUser
from social_api.users.serializers import LoginUserSerializer, RegisterUserSerializer, ProfileUserUpdateSerializer,\
    ProfileUserRetrieveSerializer


class UserAuthenticationViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def create(request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects.create_user(email=email, password=password, is_sandboxed=True, is_valid=False)

            # User authentication
            authenticated_user = authenticate(request=request, username=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                # Generating token
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Unable to authenticate user.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user:
            login(request, user)
            # Get or create token
            token, _ = Token.objects.get_or_create(user=user)
            # Return token as a part of the response
            return Response(
                {'token': token.key, 'message': 'User logged in successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response({'error': 'Unable to authenticate user.'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def logout(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)


class ProfileUserRetrieveAPI(rest_views.RetrieveAPIView):
    serializer_class = ProfileUserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileUserUpdateAPI(rest_views.UpdateAPIView):
    serializer_class = ProfileUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# class ProfileUserViewSet(viewsets.ModelViewSet):
#     def update(self, request, *args, **kwargs):
#         serializer = ProfileUserSerializer(instance=request.user, data=request.data)
#         if serializer.is_valid():
#             # Get the image from the serializer data
#             profile_picture = request.data.get('profile_picture')
#
#             # Uploading the image to Cloudinary and getting the URL
#             if profile_picture:
#                 result = upload(profile_picture)
#                 serializer.validated_data['profile_picture'] = result['secure_url']
#
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
