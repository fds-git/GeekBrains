# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class Jobparser2Pipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacancy

    def salary_handler(self, item, spider):
        if spider.name == 'sjru':
            salary = item['min_salary']
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

        if item['min_salary']:
            item['min_salary'] = int(item['min_salary'])

        if item['max_salary']:
            item['max_salary'] = int(item['max_salary'])

    def process_item(self, item, spider):
        self.salary_handler(item, spider)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
