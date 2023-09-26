from rest_framework.routers import DefaultRouter
from social_api.users.views import RegisterUserViewSet, LoginUserViewSet, LogoutUserViewSet

# Create instance of DefaultRouter
router = DefaultRouter()

# Register views with router
router.register(r'register', RegisterUserViewSet, basename='register')
router.register(r'login', LoginUserViewSet, basename='login')
router.register(r'logout', LogoutUserViewSet, basename='logout')

