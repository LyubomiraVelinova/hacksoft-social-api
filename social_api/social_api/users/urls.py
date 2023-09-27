from rest_framework import routers
from social_api.users.views import RegisterUserViewSet, LoginUserViewSet, LogoutUserViewSet, ProfileUserViewSet, \
    ProfileDetailsViewSet, UpdateProfileDetailsViewSet

# Create instance of DefaultRouter
router = routers.DefaultRouter()

# Register views with router
router.register(r'register', RegisterUserViewSet, basename='register')
router.register(r'login', LoginUserViewSet, basename='login')
router.register(r'logout', LogoutUserViewSet, basename='logout')
router.register(r'profile', ProfileUserViewSet, basename='profile')
router.register(r'details', ProfileDetailsViewSet, basename='profile_details')
router.register(r'profile-update', UpdateProfileDetailsViewSet, basename='profile_update')

