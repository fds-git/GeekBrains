# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[contains(@class, "pagination-nav")]/a/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        # Обычные + VIP объявления
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href |'
                                   '//a[@class="description-title-link js-item-link"]/@href').extract()

        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('title', '//span[contains(@class, "title-info-title-text")]/text()')
        loader.add_xpath('price', '//span[@class = "js-item-price"]/@content')
        loader.add_value('href', response.url)
        loader.add_xpath('params', '//ul[@class = "item-params-list"]/li/span/text() | //ul[@class = "item-params-list"]/li/text()')
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        yield loader.load_item()

