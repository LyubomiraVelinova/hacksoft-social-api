from django.contrib import admin
from django.urls import path, include, re_path

from social_api.swagger_config import schema_view

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    # Configure swagger and redoc urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include('social_api.users.urls')),
    path('posts/', include('social_api.posts.urls')),
    path('feed/', include('social_api.feed.urls')),
]
