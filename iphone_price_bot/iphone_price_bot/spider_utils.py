"""
This module contains utility functions for cleaning and translating data
from the website.

Mainly used in pipelines and in spiders.
"""

if __name__ == "__main__":
    exit(1)

import re


def translate_color_hu(color_hu):
    """
    Translate iPhone color names from Hungarian to English.

    Parameters:
        color_hu (str): The color name in Hungarian.

    Returns:
        str: The color name in English. If the color name is not found in the
        dictionary, the original color name is returned.
    """
    return {
        "zöld": "Green",
        "kék": "Blue",
        "sárga": "Yellow",
        "fekete": "Black",
        "rózsaszín": "Pink",
        "éjfekete": "Midnight",
        "lila": "Purple",
        "kék titán": "Blue Titanium",
        "fehér titán": "White Titanium",
        "fekete titán": "Black Titanium",
        "natúr titán": "Natural Titanium",
        "csillagfény": "Starlight",
    }.get(color_hu, color_hu)


def translate_color_se(color_se):
    """
    Translate iPhone color names from Swedish to English.

    Parameters:
        color_se (str): The color name in Swedish.

    Returns:
        str: The color name in English. If the color name is not found in the
        dictionary, the original color name is returned.
    """
    return {
        "grön": "Green",
        "blå": "Blue",
        "gul": "Yellow",
        "svart": "Black",
        "rosa": "Pink",
        "midnatt": "Midnight",
        "lila": "Purple",
        "blått titan": "Blue Titanium",
        "vit titan": "White Titanium",
        "svart titan": "Black Titanium",
        "naturlig titan": "Natural Titanium",
        "stjärnljus": "Starlight",
        "stjärnglans": "Starlight",
    }.get(color_se, color_se)


def get_country_code(url, loader_context):
    """
    Get the country code from the URL.

    Parameters:
        url (str): The URL of the website.
        loader_context (dict): The context of the loader.

    Returns:
        str: The country code.
    """
    country = loader_context["response_url"].split("/")[3]
    return "us" if country == "shop" else country


def clean_value(value):
    """
    Clean the value from unnecessary characters.
    Also, replace the comma with a dot to help make it a float number.

    Parameters:
        value (str): The value to clean.

    Returns:
        str: The cleaned value.
    """
    value = value.strip()
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    value = re.sub(r"[^\x00-\x7F]+", "", value)
    return value


def clean_model(value):
    """
    Clean the model value by removing unnecessary words and characters.

    Parameters:
        value (str): The model value to clean.

    Returns:
        str: The cleaned model value.
    """
    value = value.replace("Buy ", "")
    value = value.replace("vásárlása", "")
    value = value.replace("Köp", "")
    value = value.strip()
    value = clean_value(value=value)
    return value


def clean_capacity_unit(value):
    """
    Clean the capacity unit value by removing unnecessary characters.

    Parameters:
        value (str): The capacity unit value to clean.

    Returns:
        str: The cleaned capacity unit value.
    """
    return clean_value(value=str(value[:2]))
