# Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки,
# тема письма, текст письма полный)

# Установить selenium
# pip install selenium
# В venv закинуть chromedriver.exe

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import requests
from lxml import html
import time

def date_time_converter(date_time):
    from datetime import datetime, date, time
    months = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
              'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}
    _date, _time  = date_time.split(sep=',')
    _day, _month = _date.split(sep=' ')
    _hour, _minute = _time.split(sep=':')
    d = date(datetime.today().year ,int(months[_month]), int(_day))
    t = time(int(_hour), int(_minute))
    return datetime.combine(d, t)


headers =  {'accept':'*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

# Подключаемся к MongoDB
client = MongoClient('localhost', 27017)
mongo_base = client['mail']
collection = mongo_base['letters']

chrome_optinons = Options()
# На всю страницу
chrome_optinons.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_optinons)

driver.get('https://e.mail.ru/login')
assert "Mail" in driver.title

# Получаем элемент iframe
iframe = driver.find_element_by_class_name("ag-popup__frame__layout__iframe")

# Получаем ссылку на iframe
iframe_link = iframe.get_attribute("src")
#print(iframe_link)

# Переключаемся на iframe
driver.switch_to.frame(iframe)
assert "Mail" in driver.title

# Находим поле под логин
elem = driver.find_element_by_xpath('//input[@name = "Login"]')
# Вводим логин
elem.send_keys('study.ai_172@mail.ru')

# Находим кнопку "Ввести пароль"
elem = driver.find_element_by_xpath('//button[@data-test-id = "next-button"]')
# Нажимаем на нее
elem.click()
time.sleep(1)
# Находим поле под пароль
elem = driver.find_element_by_xpath('//input[@name = "Password"]')
# Вводим пароль
elem.send_keys('Password172')

# Нажимаем ENTER
elem.send_keys(Keys.RETURN)
assert "Mail" in driver.title
time.sleep(3)
# Собираем ссылки на письма
links = []
mails = driver.find_elements_by_xpath('//a[contains(@class, "llc")]')
for mail in mails:
    link = mail.get_attribute('href')
    if link:
        links.append(link)


# Собираем информацию с каждого письма
for link in links:
    driver.get(link)
    assert "Mail" in driver.title
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, '//span[@class = "button2__ico"]'))
    )
    from_ = driver.find_element_by_xpath('//span[@class = "letter__contact-item"]').get_attribute('title')
    date_time = driver.find_element_by_xpath('//div[@class = "letter__date"]').text
    topic = driver.find_element_by_xpath('//h2[@class = "thread__subject"]').text
    text = driver.find_element_by_xpath('//div[@class = "letter-body__body"]').text
    result = {
        'from': from_,
        'date_time': date_time_converter(date_time),
        'topic': topic,
        'text':text
    }
    collection.insert_one(result)
    driver.back()
    #time.sleep(2)

#---------------Попытка сделать сбор данных через requests-----------------------------

#cookies = driver.get_cookies()
#session = requests.Session()
#for cookie in cookies:
#    session.cookies.set(cookie['name'], cookie['value'])
#
#for link in links:
#    link_req = session.get(link, headers=headers)
#    root = html.fromstring(link_req.text)
#    from_ = root.xpath('//span[@class = "letter__contact-item"]/@title')
#    date = root.xpath('//div[@class = "letter__date"]/text()')
#    topic = root.xpath('//h2[@class = "thread__subject"]/text()')
#    result = {
#        'from': from_,
#        'date': date,
#        'topic': topic
#    }
#    collection.insert_one(result)
#-----------------------------------------------------------------------

driver.quit()