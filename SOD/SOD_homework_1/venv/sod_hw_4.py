#       Урок 4. Парсинг HTML. XPath
# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru.
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации

from pprint import pprint
from lxml import html
import requests
import pandas as pd
import time
import datetime
import numpy as np
from datetime import datetime, date, time, timedelta


headers =  {'accept':'*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

def mail_parce(headers):
    mail_link = ('https://www.mail.ru')

    req = requests.get(mail_link, headers=headers)
    root = html.fromstring(req.text)

    title = root.xpath('//div[@class="news-item__inner"]/a[last()]/text() | //div[@class="news-item__content"]/h3/text()')
    href = root.xpath('//div[@class="news-item__inner"]/a[last()]/@href | //div[@class="news-item o-media news-item_media news-item_main"]/a/@href')
    data_time = []
    source = 'mail.ru'

    # Переходим по ссылке каждой новости, чтобы вытянуть дату публикации
    for link in href:
        link_req = requests.get(link, headers=headers)
        root = html.fromstring(link_req.text)
        # Вторая часть выражения есть, потому что у кино.маил.ру верстка другая
        dt = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime | //span[@class="breadcrumbs__item js-ago"]/@datetime')
        if not dt:
            data_time.append(np.nan)
        else:
            data_time.append(dt[0])
        #time.sleep(1)

    data_time_std = []

    # Приводим data_time к стандартному типу
    for dt in data_time:
        _date,_time  = dt.split(sep='T')
        _date = _date.split(sep='-')
        _year = _date[0]
        _month =_date[1]
        _day =  _date[2]
        _time, _time_inc = _time.split(sep='+')
        _time =_time.split(sep=':')
        _time_inc = _time_inc.split(sep=':')
        _hour = _time[0]
        _minute = _time[1]
        _sec = _time[2]
        _hour_inc = _time_inc[0]

        d = date(int(_year), int(_month), int(_day))
        t = time(int(_hour), int(_minute))

        data_time_std.append(datetime.combine(d, t) + timedelta(hours=int(_hour_inc)))

    data_time = data_time_std

    #Формируем результат
    result = pd.DataFrame({'title' : title,
                           'href' : href,
                           'source': source,
                           'date_time': data_time},
                            columns=['title','href', 'date_time', 'source'])

    return result


def lenta_parce(headers):
    lenta_link = ('https://lenta.ru')
    req = requests.get(lenta_link, headers=headers)
    root = html.fromstring(req.text)
    title = root.xpath("//div[contains(@class, 'first-item')]/h2/a/text() | //div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/text()")
    href =  root.xpath("//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/@href")
    data_time = root.xpath("//div[contains(@class, 'first-item')]/h2/a/time/@datetime | //div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/time/@datetime")
    months = {'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6,
              'июля':7, 'августа':8, 'сентября':9, 'октября':10, 'ноября':11, 'декабря':12}
    data_time_std = []

    # Приводим data_time к стандартному типу
    for dt in data_time:
        _time, _date = dt.split(sep=',')
        _hour, _minute = _time.split(sep=':')
        _date = _date.split(sep=' ')
        _day = _date[1]
        _month = months[_date[2]]
        _year = _date[3]
        d = date(int(_year), int(_month), int(_day))
        t = time(int(_hour), int(_minute))
        data_time_std.append(datetime.combine(d, t))

    data_time = data_time_std

    source = 'lenta.ru'
    for i in range(len(href)):
        href[i] = lenta_link + href[i]
    #print(data_time)
    #print(title)
    result = pd.DataFrame({'title': title,
                           'href': href,
                           'date_time': data_time,
                           'source': source},
                          columns=['title', 'href', 'date_time', 'source'])

    return result

result = lenta_parce(headers)
result.to_csv('result_lenta.csv')
result_mail = mail_parce(headers)
result_mail.to_csv('result_mail.csv')
#pprint(result)
result = result.append(result_mail, ignore_index=True)
result.to_csv('result_mail_lenta.csv')
