from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


schema_view = get_schema_view(
    openapi.Info(
        title="Test Company API",
        default_version="v1",
        description="Test API Documentation ",
        terms_of_service="https://www.testcompany.com/policies/terms/",
        contact=openapi.Contact(email="test_comapny@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Swagger Wrapper
def swagger_wrapper(fields):
    documentation = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={field: openapi.Schema(type=fields[field]) for field in fields},
        )
    )
    return documentation