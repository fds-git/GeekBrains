#        Урок 5. Scrapy

# 1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
# *Наименование вакансии
# *Зарплата от
# *Зарплата до
# *Ссылку на саму вакансию
#
# *Сайт откуда собрана вакансия
# И складывал все записи в БД(любую)
#
# 2) Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob. Паука должен формировать
# item'ы по аналогичной структуре и складывать данные также в БД
# 3*) Измерить скорость сбора вакансий в проекте и сравнить ее с проектом, выполненном с использованием BS+requests

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider


if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)
    process.start()
