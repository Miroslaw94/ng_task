from django.db.models import Count
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter

from .models import Car, Rating
from .serializers import CarSerializer, RatingSerializer, CarPopularitySerializer


class CarViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarPopularityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarPopularitySerializer
    filter_backends = [OrderingFilter]
    ordering = ['-rates_number']

    def get_queryset(self):
        queryset = Car.objects.annotate(rates_number=Count('rating'))
        return queryset


class RatingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
