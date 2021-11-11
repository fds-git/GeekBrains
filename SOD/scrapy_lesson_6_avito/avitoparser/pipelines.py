# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import csv


class AvitoparserPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


# Класс для сохранения данных в CSV-файл
class CSVPipeline(object):
    def __init__(self):
        self.file = 'test.csv'
        # Открываем файл. Если он пустой, то запишем заголовки столбцов
        # из item. Если нет, то дозапишем в него данные
        with open(self.file, 'r', newline='') as csvfile:
            self.tmp_data = csv.DictReader(csvfile).fieldnames

        self.csvfile = open(self.file, 'a', newline='', encoding='UTF-8')

    def process_item(self, item, spider):
        colums = item.fields.keys()

        data = csv.DictWriter(self.csvfile, colums)
        if not self.tmp_data:
            # Формируется первая строка пустого файла
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item

    def __del__(self):
        self.csvfile.close()


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

