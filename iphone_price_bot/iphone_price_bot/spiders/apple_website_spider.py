import scrapy
import re

from iphone_price_bot.items import IphonePricesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class AppleWebsiteSpider(scrapy.Spider):
    """
    Spider for scraping iPhone prices from Apple's country specific website.
    """

    name = "apple_website_spider"

    # Explicitly set the fields to be exported. For other settings, see: settings.py
    custom_settings = {
        "FEED_EXPORT_FIELDS": ["country", "model", "capacity", "color", "price"],
    }
    allowed_domains = ["www.apple.com"]
    start_urls = [
        "https://www.apple.com/shop/buy-iphone",
        "https://www.apple.com/hu/shop/buy-iphone",
        "https://www.apple.com/se/shop/buy-iphone",
    ]
    phone_urls = []

    class IphoneItemLoader(ItemLoader):
        default_output_processor = TakeFirst()

    def parse(self, response):
        self.phone_urls = response.css(
            "div.rf-hcard.rf-hcard-40 > a::attr(href)"
        ).extract()

        for url in self.phone_urls:
            yield scrapy.Request(url, self.parse_phone)

    def parse_phone(self, response):
        phones = response.css("div.details")
        model = response.css("h1.fwl::text").extract_first()

        for phone in phones:
            phone_loader = self.IphoneItemLoader(
                item=IphonePricesItem(), selector=phone
            )
            phone_loader.context["response_url"] = response.url
            phone_loader.add_value("country", "")
            phone_loader.add_css("price", ".current_price::text")

            # capacity = phone.css("span.dimensionCapacity::text").extract_first()
            # capacity += phone.css(
            #     "span.dimensionCapacity > small::text"
            # ).extract_first()

            phone_loader.add_value("model", model)
            phone_loader.add_css("capacity", "span.dimensionCapacity::text")
            phone_loader.add_css(
                "capacity_unit", "span.dimensionCapacity > small::text"
            )
            phone_loader.add_css("color", "span.dimensionColor::text")
            yield phone_loader.load_item()
