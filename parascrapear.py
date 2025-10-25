# scrapy runspider parascrapear.py
import scrapy
# from scrapy.exporters import JsonItemExporter


class QuoteItem(scrapy.Item):
    text = scrapy.Field()


class ParascrapearSpider(scrapy.Spider):
    name = "parascrapear"
    allowed_domains = ["parascrapear.com"]
    start_urls = ["http://parascrapear.com/"]

    custom_settings = {
        "FEEDS": {
            "quotes.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "indent": 4,
            },
        },
    }

    def parse(self, response):
        print("Parseando " + response.url)

        # Follow links
        next_urls = response.css("a::attr(href)").getall()
        for next_url in next_urls:
            if next_url is not None:
                yield scrapy.Request(response.urljoin(next_url))

        # Extract quotes
        frases = response.css("q::text").getall()
        for frase in frases:
            quote_item = QuoteItem()
            quote_item["text"] = frase
            yield quote_item
