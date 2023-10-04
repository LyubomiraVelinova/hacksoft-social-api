from django.urls import path, include
from social_api.users.views import ProfileUserRetrieveAPI, ProfileUserUpdateAPI, \
    RegisterUserAPIView, LoginUserAPIView, LogoutUserAPIView

urlpatterns = [
    path('auth/', include([
        path('register/', RegisterUserAPIView.as_view(), name='register'),
        path('login/', LoginUserAPIView.as_view(), name='login'),
        path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    ])),
    path('profile/', include([
        path('details/', ProfileUserRetrieveAPI.as_view(), name='profile details'),
        path('update/', ProfileUserUpdateAPI.as_view(), name='profile update'),
    ])),
]
