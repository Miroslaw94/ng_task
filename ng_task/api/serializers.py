from rest_framework import serializers

from .models import Car, Rating
from .utils import car_exists


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField(method_name='calculate_avg_rating')

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']

    def validate(self, data):
        if car_exists(data['make'], data['model']):
            return data
        else:
            raise serializers.ValidationError("That car doesn't exist. Please provide real car make and model name. ")

    def calculate_avg_rating(self, instance):
        ratings = Rating.objects.filter(car_id=instance.id).all()
        ratings_sum = 0.0
        if ratings:
            ratings_sum = float(sum(r.rating for r in ratings) / len(ratings))
        return round(ratings_sum, 1)


class CarPopularitySerializer(serializers.ModelSerializer):
    rates_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['car_id', 'rating']
