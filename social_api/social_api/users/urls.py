from django.urls import path, include
from rest_framework import routers
from social_api.users.views import UserAuthenticationViewSet, ProfileUserRetrieveAPI, ProfileUserUpdateAPI, UserListView

# Create instance of DefaultRouter
router = routers.DefaultRouter()

# Register views with router
router.register(r'authentication', UserAuthenticationViewSet, basename='authentication')

urlpatterns = [
    path('', UserListView.as_view()),
    path('profile/', include([
        path('details/', ProfileUserRetrieveAPI.as_view(), name='profile details'),
        path('update/', ProfileUserUpdateAPI.as_view(), name='profile update'),
    ])),
]

urlpatterns += router.urls
