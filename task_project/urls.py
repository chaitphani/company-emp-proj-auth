from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("company.urls")),
    path('', include("super_admin.urls")),
    path('', include("employee.urls")),
    path('', include("project.urls"))    
]
