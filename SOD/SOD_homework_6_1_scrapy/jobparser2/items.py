# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# При переходе на работу через ItemLoader в поля item попадают списки из одного элемента
# нужно извлекать их с помощью TakeFirst
from scrapy.loader.processors import TakeFirst


def concat(values):
    result = ''
    for value in values:
        if value is not None and value != '':
            result += value
    if result == '':
        return None
    else:
        return result


class Jobparser2Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    href = scrapy.Field(output_processor=TakeFirst())
    company = scrapy.Field(output_processor=TakeFirst())
    min_salary = scrapy.Field(output_processor=concat)
    max_salary = scrapy.Field(output_processor=TakeFirst())
    money_type = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
    pass


