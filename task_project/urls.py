from django.contrib import admin
from django.urls import path, include
from swagger.documentation import schema_view
from company.urls import urlpatterns as company_url_pattern
from super_admin.urls import urlpatterns as super_admin_url_pattern
from employee.urls import urlpatterns as employee_url_pattern
from project.urls import urlpatterns as project_url_pattern

# urlpatterns = [

#     path('admin/', admin.site.urls),
#     path('', include("company.urls")),
#     path('', include("super_admin.urls")),
#     path('', include("employee.urls")),
#     path('', include("project.urls"))
    
# ]


urlpatterns =(
   [
        path('admin/', admin.site.urls),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    + company_url_pattern
    + super_admin_url_pattern
    + employee_url_pattern
    + project_url_pattern
)
