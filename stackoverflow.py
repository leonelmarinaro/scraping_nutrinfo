from scrapy.item import Item, Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class Pregunta(Item):
    # id = Field()
    pregunta = Field()
    # descripcion = Field()


class StackOverflowSpider(Spider):
    name = "stackoverflow"
    # custom_settings = {
    #     "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    # }

    start_urls = ["https://stackoverflow.com/questions"]

    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath(
            '//div[@id="questions"]//div[contains(@data-post-type-id, "1")]'
        )
        for pregunta in preguntas:
            item = ItemLoader(item=Pregunta(), selector=pregunta)
            item.add_xpath("pregunta", ".//h3/a/text()")
            # item.add_xpath(
            #     "descripcion", ".//div[@class='s-post-summary--content-excerpt']/text()"
            # )
            # item.add_value("id", idx)
            yield item.load_item()
