# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class EventItem(scrapy.Item):
    event_title = Field()
    sport = Field()
    sport_discipline = Field()
    event_description = Field()
    event_image = Field()
    organizer = Field()
    event_website = Field()
    event_start_date = Field()
    event_end_date = Field()
    registration_start_date = Field()
    registration_end_date = Field()
    location = Field()
    event_fee = Field()
    payment_destination = Field()
    schedule = Field()
    event_social_links = Field()
    event_accommodations = Field()
    event_regulation = Field()
    event_sponsors = Field()
    external_registration_url = Field()
    region = Field()
    country = Field()

    event_source_url = Field()
    source = Field()
    content = Field()
