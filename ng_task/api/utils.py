import requests

from rest_framework.serializers import ValidationError


CAR_API_ROOT = "https://vpic.nhtsa.dot.gov/api/"
ENDPOINT_MODELS_FOR_MAKE = CAR_API_ROOT + "/vehicles/GetModelsForMake/{}?format=json"


def car_exists(make: str, model: str) -> bool:
    try:
        response = requests.get(ENDPOINT_MODELS_FOR_MAKE.format(make))
    except requests.exceptions.RequestException:
        raise ValidationError(
            'An error occurred while trying to connect with external service. Please, try again later. '
        )

    response_data = response.json()
    if response_data['Count'] > 0:
        if any(car['Model_Name'] == model for car in response_data['Results']):
            return True
    return False
