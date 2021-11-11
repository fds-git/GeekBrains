#    Урок 6. Scrapy. Парсинг фото и файлов

# Взять авито Авто. Собирать с использованием ItemLoader следующие данные:
#
# Название
# Все фото
# параметры Авто
# С использованием output_processor и input_processor реализовать очистку и преобразование данных.
# Значения цен должны быть в виде числового значения.


# Установка фреймворка
# pip install scrapy
# for work with photos
# pip install pillow
# for work with databases
# pip install pymongo
# create project in current directory
# scrapy startproject avitoparser .
# create spider
# scrapy genspider avito avito.ru
# don't forget to create runner near scrapy.cfg


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider)
    process.start()
