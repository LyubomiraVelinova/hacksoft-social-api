from django.contrib.auth import login, logout
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics as api_views

from social_api.users.models import CustomUser
from social_api.users.serializers import LoginUserSerializer, RegisterUserSerializer, ProfileUserUpdateSerializer, \
    ProfileUserRetrieveSerializer
'''
Public API for registration
Users can authenticate using email & password.
'''


class RegisterUserAPIView(api_views.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            # When a new user is registered, that user is “sandboxed”
            data = {}
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save(is_sandboxed=True, is_valid=False)
                token = Token.objects.get_or_create(user=account)[0].key
                data["message"] = "User registered successfully"
                data["email"] = account.email
                data["token"] = token

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            raise ValidationError({"400": str(e)})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})


'''
API for logging in.
Users can authenticate using email & password.
'''


class LoginUserAPIView(api_views.CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = {}
        email = self.request.data.get('email')

        try:
            account = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError({"400": "Account doesn't exist"})

        token, _ = Token.objects.get_or_create(user=account)

        login(request, account)
        data["message"] = "User logged in"
        data["email"] = account.email

        response_data = {"data": data, "token": token.key}

        return Response(response_data)


'''
API for logging out
'''


class LogoutUserAPIView(api_views.CreateAPIView):
    def create(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response('User logged out successfully', status=status.HTTP_200_OK)


# PROFILES

'''
API for getting the data for the currently logged-in user
Accessible for authenticated users only
'''


class ProfileUserRetrieveAPI(api_views.RetrieveAPIView):
    serializer_class = ProfileUserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


'''
API for updating the user data (everything without email / password) for the currently logged-in user.
Accessible for authenticated users only.
'''


class ProfileUserUpdateAPI(api_views.UpdateAPIView):
    serializer_class = ProfileUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
