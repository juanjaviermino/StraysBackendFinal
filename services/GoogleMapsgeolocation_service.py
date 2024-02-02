import requests
from .igeolocation_service import IGeoLocationService

class GoogleMapsGeoLocationService(IGeoLocationService):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_city_name_by_coordinates(self, lat, lng):
        params = {
            "latlng": f"{lat},{lng}",
            "key": self.api_key,
            "language": "es"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                for component in results[0]['address_components']:
                    if "locality" in component['types']:
                        return component['long_name']
                for component in results[0]['address_components']:
                    if "administrative_area_level_2" in component['types']:
                        return component['long_name']
            return None
        else:
            raise Exception(f"Error al obtener la ubicación geográfica: {response.status_code}")
