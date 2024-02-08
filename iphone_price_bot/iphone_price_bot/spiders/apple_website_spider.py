import scrapy
import re

from iphone_price_bot.items import IphonePricesItem


def get_country_code(url):
    country = url.split("/")[3]
    return "us" if country == "shop" else country


def clean_value(value):
    value = value.strip()
    value = value.replace(" ", "")
    value = re.sub(r"[^\x00-\x7F]+", "", value)
    return value


class AppleWebsiteSpider(scrapy.Spider):
    name = "apple_website_spider"
    allowed_domains = ["www.apple.com"]
    start_urls = [
        "https://www.apple.com/shop/buy-iphone",
        "https://www.apple.com/hu/shop/buy-iphone",
        "https://www.apple.com/se/shop/buy-iphone",
    ]
    phone_urls = []

    def parse(self, response):
        self.phone_urls = response.css(
            "div.rf-hcard.rf-hcard-40 > a::attr(href)"
        ).extract()

        for url in self.phone_urls:
            yield scrapy.Request(url, self.parse_phone)

    def parse_phone(self, response):
        phones = response.css("div.details")
        model = response.css("h1.fwl::text").extract_first()

        if model:
            model = model.replace("Buy ", "")
            model = model.replace("vásárlása", "")
            model = model.replace("Köp", "")
            model = clean_value(value=model)

        for phone in phones:
            price = phone.css(".current_price::text").extract_first()
            capacity = phone.css("span.dimensionCapacity::text").extract_first()
            capacity += phone.css(
                "span.dimensionCapacity > small::text"
            ).extract_first()

            if price:
                yield {
                    "country": get_country_code(response.url),
                    "model": model,
                    "price": clean_value(price),
                    "capacity": capacity,
                    "color": phone.css("span.dimensionColor::text").extract_first(),
                }
