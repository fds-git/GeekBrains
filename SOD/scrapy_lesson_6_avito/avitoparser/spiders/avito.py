# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        #print(ads_links)
        for link in ads_links:
            print(link)
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        #photos = response.xpath(
        #'//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        #temp = AvitoparserItem(photos=photos)
        #yield temp
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        yield loader.load_item()
