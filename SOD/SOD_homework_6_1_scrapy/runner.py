# pip install scrapy
# Для работы с фото
# pip install pillow
# Для работы с БД
# pip install pymongo
# Создание проекта в текущей директории
# scrapy startproject avitoparser .
# Создание паука
# scrapy genspider avito avito.ru
# Не забыть создать сам runner рядом с scrapy.cfg

# Это дальнейшее развитие SOD_homework_5, где сбор данных осуществлен через ItemLoader

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser2 import settings
from jobparser2.spiders.hhru import HhruSpider
from jobparser2.spiders.sjru import SjruSpider


if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)
    process.start()
