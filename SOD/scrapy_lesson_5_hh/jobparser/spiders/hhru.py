# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&showClusters=false']

    def parse(self, response): # Точка входа, отсюда начинаем работать
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first() #Ccskrf на следю страницу
        yield response.follow(next_page, callback=self.parse) # Переходим на следующую страницу и возвращаемся

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract() # Извлекаем ссылки на все вакансии

        for link in vacansy:
            yield response.follow(link, self.vacansy_parse) #Переходим на страницы вакансий

    def vacansy_parse(self, response): #Собираем информацию со страницы
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        yield JobparserItem(name=name, salary=salary) #Формируем item

