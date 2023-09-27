from rest_framework import routers

from social_api.posts.views import LikeListCreateView, PostListCreateView

# Create instance of DefaultRouter
router = routers.DefaultRouter()

# Register views with router
router.register(r'posts', PostListCreateView, basename='post')
router.register(r'likes', LikeListCreateView, basename='likes')
