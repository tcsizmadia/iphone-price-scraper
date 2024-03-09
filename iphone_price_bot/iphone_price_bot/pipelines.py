# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from .spider_utils import translate_color_hu, translate_color_se


class IphonePriceSpiderPipeline:
    """
    Pipeline for processing iPhone price items.

    This pipeline checks if the item has a "price" field. If it does, it adds the "capacity_unit" to the "capacity" field,
    removes the "capacity_unit" field, and returns the modified item. If the item does not have a "price" field, it raises
    a DropItem exception to discard the item.

    Args:
        item (dict): The item to be processed.

    Returns:
        dict: The processed item.

    Raises:
        DropItem: If the item does not have a "price" field.
    """

    def process_item(self, item, spider):
        if "price" in item:
            item["capacity"] = item["capacity"] + item["capacity_unit"]
            del item["capacity_unit"]
            return item
        else:
            raise DropItem()


class IphoneColorConverterPipeline:
    """
    Pipeline for converting iPhone color based on country.

    This pipeline converts the color field of the item based on the country field. If the country is "hu", it uses the
    translate_color_hu function to translate the color. If the country is "se", it uses the translate_color_se function.
    The converted color is then assigned back to the color field of the item.

    Args:
        item (dict): The item to be processed.

    Returns:
        dict: The processed item.
    """

    def convert_color(self, item):
        if item["country"] == "hu":
            item["color"] = translate_color_hu(item["color"])
        elif item["country"] == "se":
            item["color"] = translate_color_se(item["color"])
        return item["color"]

    def process_item(self, item, spider):
        item["color"] = self.convert_color(item=item)
        return item


class IphonePriceConvertPricePipeline:
    """
    Pipeline for converting iPhone price to USD based on country.

    This pipeline cleans the currency value by removing commas, dollar signs, and country-specific currency symbols.
    It then converts the cleaned price to USD based on the country field of the item. The converted price is assigned
    back to the price field of the item.

    Args:
        item (dict): The item to be processed.

    Returns:
        dict: The processed item.
    """

    def clean_currency(self, value):
        value = (
            value.lower()
            .replace(",", ".")
            .replace("$", "")
            .replace("ft", "")
            .replace("kr", "")
        )

        if value.count(".") > 1:
            value = value.replace(".", "", value.count(".") - 1)

        return value

    """
    Convert the price to USD based on the country field of the item.

    Args:
        price (str): The price to be converted.
        country (str): The country of the item.

    Returns:
        float: The converted price in USD.
    """

    def convert_to_usd(self, price, country):
        price = float(price)
        return {
            "us": price,  # 1 USD = 1 USD :)
            "hu": price * 0.0034,  # 1 HUF = 0.0034 USD
            "se": price * 0.11,  # 1 SEK = 0.11 USD
        }.get(country, "N/A")

    def process_item(self, item, spider):
        item["price"] = self.convert_to_usd(
            price=self.clean_currency(value=item["price"]), country=item["country"]
        )

        return item
