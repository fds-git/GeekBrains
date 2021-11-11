# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def take_first_int(values):
    for value in values:
        if value is not None and value != '':
            return int(value)


def cleaner_params(values):
    result = dict()
    previous = ''
    for val in values:
        if val == ' ':
            previous = ' '
            continue
        elif previous == ' ':
            previous = val
            continue
        else:
            result[previous] = val
    return result


class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    href = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(output_processor=take_first_int)
    params = scrapy.Field(output_processor=cleaner_params)
    pass
