from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Car, Rating


class CarsAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.cars_url = reverse('cars-list')
        Car.objects.create(make='Ford', model='Focus')
        Car.objects.create(make='Ford', model='Mondeo')

    def test_GET_cars_list(self):
        response = self.client.get(self.cars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(any(car['model'] == 'Focus' for car in response.data))
        self.assertTrue(any(car['model'] == 'Mondeo' for car in response.data))

    def test_GET_specific_car(self):
        test_car = Car.objects.get(model='Focus')
        response = self.client.get(reverse('cars-detail', args=(test_car.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['make'], 'Ford')
        self.assertEqual(response.data['model'], 'Focus')

    def test_GET_specific_car_invalid_id(self):
        response = self.client.get(reverse('cars-detail', args=(100,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found', str(response.data))

    def test_POST_car(self):
        car_payload = {
            'make': 'BMW',
            'model': 'M5'
        }
        response = self.client.post(self.cars_url, car_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['make'], 'BMW')
        self.assertEqual(response.data['model'], 'M5')

    def test_POST_car_with_invalid_data(self):
        car_payload = {
            'make': 'not_existing',
            'model': 'wrong_model'
        }
        response = self.client.post(self.cars_url, car_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("car doesn't exist", str(response.data))

    def test_DELETE_car(self):
        test_car = Car.objects.get(model='Mondeo')
        response = self.client.delete(reverse('cars-detail', args=(test_car.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_DELETE_car_invalid_id(self):
        response = self.client.delete(reverse('cars-detail', args=(100,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found', str(response.data))


class PopularAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.popular_cars_url = reverse('popular-list')
        test_car_1 = Car.objects.create(make='Ford', model='Focus')
        test_car_2 = Car.objects.create(make='Ford', model='Mondeo')
        test_car_3 = Car.objects.create(make='Toyota', model='Yaris')
        Car.objects.create(make='BMW', model='M5')
        Rating.objects.create(car_id=test_car_1, rating=5)
        Rating.objects.create(car_id=test_car_2, rating=5)
        Rating.objects.create(car_id=test_car_2, rating=5)
        Rating.objects.create(car_id=test_car_2, rating=4)
        Rating.objects.create(car_id=test_car_2, rating=5)
        Rating.objects.create(car_id=test_car_3, rating=5)
        Rating.objects.create(car_id=test_car_3, rating=4)

    def test_GET_popular_cars_list(self):
        response = self.client.get(self.popular_cars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['model'], 'Mondeo')
        self.assertEqual(response.data[0]['rates_number'], 4)
        self.assertEqual(response.data[3]['model'], 'M5')
        self.assertEqual(response.data[3]['rates_number'], 0)


class RateAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.rate_url = reverse('rating-list')
        Car.objects.create(make='Ford', model='Focus')

    def test_POST_rating(self):
        test_car = Car.objects.get(model='Focus')
        car_rating_payload = {
            'car_id': test_car.id,
            'rating': 5
        }
        response = self.client.post(self.rate_url, car_rating_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(dict(response.data), car_rating_payload)

    def test_POST_rating_with_wrong_id(self):
        car_rating_payload = {
            'car_id': 100,
            'rating': 5
        }
        response = self.client.post(self.rate_url, car_rating_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(response.data))
