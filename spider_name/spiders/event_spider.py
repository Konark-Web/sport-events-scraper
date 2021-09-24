import json
import re
from datetime import datetime

import requests
import scrapy
from spider_name.exceptions import EventsNotFound
from spider_name.geo_functions import GeoLocation
from spider_name.items import EventItem
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Response

from ..settings import logger


def in_dictionary(key, dict):
    if key in dict:
        return dict[key]

    return ''


class EventSpider(scrapy.Spider):
    name = 'event_spider'
    allowed_domains = ['example.com', 'results.example.com', 'eventresults-api.example.com', 'live.example.com']
    start_urls = ['https://eventresults-api.example.com/api/events/recent?eventType=null&maxNumberOfItems=15&offset'
                 '=0&q=&year=']

    def parse(self, response, **kwargs):
        offset = kwargs.get('offset', 0)
        events = ''
        events_len = 0
        response_json = json.loads(response.body)

        if offset == 0 and 'events' not in response_json:
            date_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            logger.error('[{0}] No objects for parsing were found on {1}'.format(date_now, response.request.url))
            raise EventsNotFound('No objects for parsing were found.')

        offset += 15
        url = 'https://eventresults-api.example.com/api/events/recent?eventType=null&maxNumberOfItems=15&offset=' \
              '{}&q=&year='.format(str(offset))

        if 'events' in response_json:
            events = response_json['events']
            events_len = len(events)

        for event in events:
            event_title = in_dictionary('name', event)
            sport = in_dictionary('activity', event)
            event_image = in_dictionary('backgroundPhotoUrl', event)
            organizer = in_dictionary('organization', event)
            city = in_dictionary('city', event)
            country_code = in_dictionary('countryCode', event)
            event_source_url = 'https://results.example.com/events/' + str(in_dictionary('id', event))
            region = ''
            lat = 0
            lon = 0

            event_start_date = in_dictionary('date', event)
            if event_start_date:
                try:
                    new_format_date = re.sub(r'(?<=[+=][0-9]{2}):', '', event_start_date)
                    if new_format_date:
                        event_start_date = datetime.strptime(new_format_date, '%Y-%m-%dT%H:%M:%S%z').strftime(
                            '%Y-%m-%d')
                except ValueError:
                    event_start_date = in_dictionary('displayDate', event)
                    event_start_date = datetime.strptime(event_start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

            if not event_start_date:
                event_start_date = in_dictionary('displayDate', event)
                event_start_date = datetime.strptime(event_start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

            if 'latitude' in event and 'longitude' in event:
                if event['latitude'] != 0 and event['longitude'] != 0:
                    lat = event['latitude']
                    lon = event['longitude']

            if not lat and not lon:
                if city:
                    geolocation = GeoLocation().get_geo_by_place(city, country_code)

                    lat = geolocation['lat']
                    lon = geolocation['lon']
                    region = geolocation['state']

                    if not country_code:
                        country_code = geolocation['country_code']

            if lat and lon and event_start_date:
                geo = GeoLocation().get_geo_by_coordinates(lat, lon)

                if not city:
                    city = geo['city']

                if not region or not country_code:
                    if not region:
                        region = geo['state']

                    if not country_code:
                        country_code = geo['country_code']

                yield EventItem(event_title=event_title,
                                sport=sport,
                                sport_discipline='Other',
                                event_image=event_image,
                                organizer=organizer,
                                event_start_date=event_start_date,
                                location={
                                    'link': f"https://www.google.com/maps/search/?api=1&query={lat},{lon}",
                                    'description': city
                                },
                                region=region,
                                country=country_code,
                                event_source_url=event_source_url,
                                source='example',
                                content='event')

        if type(events) is str or (type(events) is list and events_len):
            yield scrapy.Request(url, cb_kwargs={'offset': offset})
