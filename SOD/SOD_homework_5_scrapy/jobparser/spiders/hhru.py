# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=python']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, self.vacansy_parse)

    def vacansy_parse(self, response):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        #href = response.css('div[itemscope="itemscope"] meta[itemprop="url"]::attr(content)').extract_first()
        href = response.url
        company = response.css('span[itemprop="name"]::text').extract_first()
        min_salary = response.css('meta[itemprop="minValue"]::attr(content)').extract_first()
        max_salary = response.css('meta[itemprop="maxValue"]::attr(content)').extract_first()
        money_type = response.css('meta[itemprop="currency"]::attr(content)').extract_first()
        source = 'hh.ru'

        yield JobparserItem(name=name, href=href, company=company, min_salary=min_salary,
                            max_salary=max_salary, money_type=money_type, source=source)
