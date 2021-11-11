# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.f-test-vacancy-item a[target="_blank"]::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, self.vacansy_parse)

    def vacansy_parse(self, response):
        name = response.css('h1._3mfro::text').extract_first()
        href = response.url
        company = response.css('a.icMQ_ h2._3mfro::text').extract_first()
        # В min_salary будет список строк, содержащий информацию о зарплате
        min_salary = response.css('span[class = "_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] *::text').extract()
        print(min_salary)
        #max_salary = response.css('meta[itemprop="maxValue"]::attr(content)').extract_first()
        #money_type = response.css('meta[itemprop="currency"]::attr(content)').extract_first()
        source = 'superjob.ru'

        yield JobparserItem(name=name, href=href, company=company, min_salary=min_salary,
                            max_salary=None, money_type='RUR', source=source)
