from .models import Place

import requests


def get_place(api_key, address):
    place, _ = Place.objects.get_or_create(
        address=address
    )
    if not place.longitude or not place.latitude:
        try:
            place.longitude, place.latitude = fetch_coordinates(api_key, address)
            place.save()

        except requests.exceptions.HTTPError:
            return None

        except requests.exceptions.ConnectionError:
            return None

    return place


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        }
    )
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None, None

    most_relevant = found_places[0]
    longitude, latitude = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return longitude, latitude
