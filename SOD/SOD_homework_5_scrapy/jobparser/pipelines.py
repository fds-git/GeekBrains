# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacancy

    def process_item(self, item, spider):
        # Формируем одну строку из списка строк с информацией о зарплате
        if spider.name == 'sjru':
            salary = ''
            for i in item['min_salary']:
                salary += i

            # Обрабатываем информацию о зарплате
            if '—' in salary:
                min_salary = salary.split('—')[0]
                max_salary = salary.split('—')[1]
                min_salary = ''.join(filter(lambda x: x.isdigit(), min_salary))
                max_salary = ''.join(filter(lambda x: x.isdigit(), max_salary))

            elif 'от' in salary:
                # compensation1 = compensation[3:]
                min_salary = ''.join(filter(lambda x: x.isdigit(), salary))
                max_salary = None
            elif 'договорённости' in salary:
                min_salary = None
                max_salary = None

            elif 'до' in salary:
                min_salary = None
                max_salary = ''.join(filter(lambda x: x.isdigit(), salary))

                # Если одно значение без от и до
            else:
                min_salary = ''.join(filter(lambda x: x.isdigit(), salary))
                max_salary = None

            item['min_salary'] = min_salary
            item['max_salary'] = max_salary

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
