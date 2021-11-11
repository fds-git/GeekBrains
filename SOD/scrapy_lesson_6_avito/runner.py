# Framework install
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

# Pipeline DataBasePipeline are disabled in settings.py
# MongoDB server start with command: mongod.exe --dbpath D:\bases

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
