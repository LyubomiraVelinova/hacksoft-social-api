from django.urls import path, include
from rest_framework import routers
from social_api.users.views import UserAuthenticationViewSet, ProfileUserRetrieveAPI, ProfileUserUpdateAPI

# Create instance of DefaultRouter
router = routers.DefaultRouter()

# Register views with router
router.register(r'authentication', UserAuthenticationViewSet, basename='authentication')

urlpatterns = [
    path('profile/', include([
        path('details/', ProfileUserRetrieveAPI, name='profile details'),
        path('update/', ProfileUserUpdateAPI, name='profile update'),
    ])),
]

urlpatterns += router.urls
