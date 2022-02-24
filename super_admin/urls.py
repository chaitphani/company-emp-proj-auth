from django.urls import path,include
from rest_framework.routers import DefaultRouter
from super_admin.views.authorization import RegisterAPI,LoginAPI



router = DefaultRouter()
router.register('register',RegisterAPI,basename='Register')
router.register('login',LoginAPI,basename='Login')


urlpatterns = [
    path('', include(router.urls)),
]