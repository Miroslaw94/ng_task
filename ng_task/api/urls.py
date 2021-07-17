from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r'cars', views.CarViewSet, basename='cars')
router.register(r'rate', views.RatingViewSet)
router.register(r'popular', views.CarPopularityViewSet, basename='popular')

urlpatterns = [
    path('', include(router.urls))
]
