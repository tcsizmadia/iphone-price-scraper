# Scrapy Sample Project: Apple iPhone Price Scraper Bot

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This is a sample project to demonstrate how to use [Scrapy](https://scrapy.org/) to scrape data from a website. The bot scrapes the prices of Apple iPhones from Apple's official websites in different countries. The scraped data is then saved to a CSV file or any other format that is supported by Scrapy.

Please note, this is a demonstration project and should not be used for anything other than educational purposes.

## Requirements

- Python 3.6 or later
- Scrapy

## Installation

1. Clone the repository.
2. Install Python 3.6 or later.
3. Install scrapy using pip:
   ```bash
   pip install scrapy
   ```

## Usage

To run the bot, navigate to the project directory and run the following command:

```bash
scrapy crawl iphone_price_bot -o iphone_prices.csv
```

This will run the bot and save the scraped data to a CSV file named `iphone_prices.csv`. 

You can also save the scraped data to other formats such as JSON, XML, or even a database. For more information, please refer to the [Scrapy documentation](https://docs.scrapy.org/en/latest/topics/feed-exports.html).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).
