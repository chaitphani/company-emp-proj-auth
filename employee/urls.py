from django.urls import path,include
from rest_framework.routers import DefaultRouter
from employee.views.employee_views import EmployeeAPI



router = DefaultRouter()
router.register('employee',EmployeeAPI,basename='Employee')


urlpatterns = [
    path('', include(router.urls)),
]