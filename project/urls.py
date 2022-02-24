from django.urls import path,include
from rest_framework.routers import DefaultRouter
from project.views.project_views import ProjectAPI



router = DefaultRouter()
router.register('project',ProjectAPI,basename='Project')


urlpatterns = [
    path('', include(router.urls)),
]