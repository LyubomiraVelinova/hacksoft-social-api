from rest_framework import routers
from social_api.users.views import UserAuthenticationViewSet, ProfileUserViewSet

# Create instance of DefaultRouter
router = routers.DefaultRouter()

# Register views with router
router.register(r'authentication', UserAuthenticationViewSet, basename='authentication')
router.register(r'profile', ProfileUserViewSet, basename='profile')


