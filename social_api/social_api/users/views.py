from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

from social_api.users.models import CustomUser
from social_api.users.serializers import LoginUserSerializer, RegisterUserSerializer, ProfileUserSerializer


class RegisterUserViewSet(viewsets.ViewSet):
    @staticmethod
    def create(request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects.create_user(email=email, password=password, is_sandboxed=True)

            # User authentication
            authenticated_user = authenticate(request=request, username=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                # Generating token
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                return Response({'message': 'User registered successfully'})
            else:
                return Response({'error': 'Unable to authenticate user.'})
        return Response(serializer.errors, status=400)


# class ApiLoginView(ObtainAuthToken):
#     pass

class LoginUserViewSet(viewsets.ViewSet):
    @staticmethod
    def create(request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)
        # Return token as a part of the response
        return Response(
            {'token': token.key, 'message': 'User logged in successfully.'},
            status=status.HTTP_201_CREATED
        )


class LogoutUserViewSet(viewsets.ViewSet):
    # Invalidate user`s token
    @staticmethod
    def logout(request):
        request.auth.delete()
        return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)


# All functionality related to user profiles,
class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass
