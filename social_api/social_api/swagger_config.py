from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='social_api',
        default_version='v1',
        description='This Django application serves as the backend for user management, post creation, '
                    'and feed retrieval, catering to the requirements of the associated React frontend application.',
        contact=openapi.Contact(email='velinova.lyubomira@gmail.com'),
        license=openapi.License(name='My License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
