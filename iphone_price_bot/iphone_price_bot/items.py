# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from . import spider_utils


class IphonePricesItem(scrapy.Item):

    country = scrapy.Field(input_processor=MapCompose(spider_utils.get_country_code))
    model = scrapy.Field(input_processor=MapCompose(spider_utils.clean_model))
    capacity = scrapy.Field(input_processor=MapCompose(spider_utils.clean_value))
    capacity_unit = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(spider_utils.clean_value))
