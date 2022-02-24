from django.urls import path,include
from rest_framework.routers import DefaultRouter
from company.views.company_views import CompanyAPI



router = DefaultRouter()
router.register('company',CompanyAPI,basename='Company')


urlpatterns = [
    path('', include(router.urls)),
]