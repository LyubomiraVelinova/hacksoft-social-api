from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets

from social_api.users.serializers import LoginUserSerializer, RegisterUserSerializer


# class RegisterUserView(api_views.CreateAPIView):
#     serializer_class = UserSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginUserView(api_views.CreateAPIView):
#     serializer_class = LoginUserSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # Get or create token
#         token, _ = Token.objects.get_or_create(user=user)
#         # Return token as a part of the response
#         return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class RegisterUserViewSet(viewsets.ViewSet):
    @staticmethod
    def create(request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.save(is_sandboxed=True)
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=400)


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
