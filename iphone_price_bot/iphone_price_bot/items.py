# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IphonePricesItem(scrapy.Item):
    country = scrapy.Field()
    model = scrapy.Field()
    capacity = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
