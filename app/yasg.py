from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Hammer System API",
      default_version='v1',
      description="Documentation test task",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="flashvita@yandex.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)