import requests


def get_value_json(json, *values):
    for value in values:
        if value in json:
            return json[value]

    return ''


class GeoLocation:
    def get_geo_by_place(self, place, country_code=''):
        geo = {
            'lat': 0,
            'lon': 0,
            'state': '',
            'country': '',
            'country_code': '',
            'city': ''}

        if not place:
            return geo

        params = {'q': place,
                  'countrycodes': country_code,
                  'extratags': '1',
                  'format': 'jsonv2',
                  'addressdetails': '1',
                  'accept-language': 'en'}

        response = requests.get('https://nominatim.openstreetmap.org/search.php', params=params)

        if response.status_code == 200:
            response_json = response.json()

            if not len(response_json):
                return geo

            for location in response_json:
                place_category = get_value_json(location, 'category')
                if place_category == 'waterway':
                    continue

                geo['lat'] = get_value_json(location, 'lat')
                geo['lon'] = get_value_json(location, 'lon')

                if 'address' not in location:
                    continue

                address_json = location['address']
                geo['country'] = get_value_json(address_json, 'country')
                geo['country_code'] = get_value_json(address_json, 'country_code').upper()

                geo['city'] = get_value_json(address_json, 'village', 'town', 'city')
                geo['state'] = get_value_json(address_json, 'state', 'county', 'region')

                if not geo['state']:
                    capital = None

                    if 'extratags' in location:
                        extratags_json = location['extratags']
                        capital = get_value_json(extratags_json, 'capital')

                    if capital and capital == 'yes' and get_value_json(address_json, 'city'):
                        geo['state'] = get_value_json(address_json, 'city')
                    elif self.is_capital_by_geo(geo['lat'], geo['lon'], '10') and get_value_json(address_json, 'city'):
                        geo['state'] = get_value_json(address_json, 'city')

                break

        return geo

    def is_capital_by_geo(self, lat, lon, zoom='18'):
        if lat and lon:
            params = {'lat': lat,
                      'lon': lon,
                      'zoom': zoom,
                      'extratags': '1',
                      'accept-language': 'en',
                      'format': 'jsonv2'}

            response = requests.get('https://nominatim.openstreetmap.org/reverse.php', params=params)

            if response.status_code == 200:
                response_json = response.json()

                if 'extratags' in response_json:
                    if 'capital' in response_json['extratags']:
                        if response_json['extratags']['capital'] == 'yes':
                            return True

        return False

    def get_geo_by_coordinates(self, lat, lon, zoom='18'):
        geo = {
            'city': '',
            'state': '',
            'country': '',
            'country_code': ''
        }

        if not lat and not lon:
            return geo

        params = {
            'lat': lat,
            'lon': lon,
            'zoom': zoom,
            'extratags': '1',
            'accept-language': 'en',
            'format': 'jsonv2'}

        response = requests.get('https://nominatim.openstreetmap.org/reverse.php', params=params)

        if response.status_code == 200:
            response_json = response.json()

            if not len(response_json):
                return geo

            if 'address' not in response_json:
                return geo

            address_json = response_json['address']
            geo['country'] = get_value_json(address_json, 'country')
            geo['country_code'] = get_value_json(address_json, 'country_code').upper()

            geo['city'] = get_value_json(address_json, 'village', 'town', 'city')
            geo['state'] = get_value_json(address_json, 'state', 'county', 'region')

            if not geo['state']:
                capital = None

                if 'extratags' in response_json:
                    extratags_json = response_json['extratags']
                    capital = get_value_json(extratags_json, 'capital')

                if capital and capital == 'yes' and get_value_json(address_json, 'city'):
                    geo['state'] = get_value_json(address_json, 'city')
                elif self.is_capital_by_geo(geo['lat'], geo['lon'], '10') and get_value_json(address_json, 'city'):
                    geo['state'] = get_value_json(address_json, 'city')

        return geo
