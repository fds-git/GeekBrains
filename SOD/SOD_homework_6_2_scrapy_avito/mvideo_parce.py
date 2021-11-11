# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и
# складывает данные в БД. Магазины можно выбрать свои. Главный критерий выбора:
# динамически загружаемые товары

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

headers =  {'accept':'*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

# Подключаемся к MongoDB
client = MongoClient('localhost', 27017)
mongo_base = client.selenium_mvideo
collection = mongo_base['mvideo']

# Окно на всю страницу
chrome_optinons = Options()
chrome_optinons.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_optinons)

driver.get('https://www.mvideo.ru/')
#print(driver.title)
assert 'М.Видео' in driver.title


# Прокручиваем ленту "Хиты продаж", чтобы в коде страницы были все 20 элементов
while True:
    try:
        # Баннер не закрываю, так как он при старте страницы не всегда появляется и не влияет на работу
        # Используется не element_to_be_clickable потому что этот элемент становится невидимым постоянно
        button = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//div[@class = "gallery-layout"][1]//a[@class = "next-btn sel-hits-button-next"]'))
        )
        # button.click() не работает
        button.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)
        break


# Собираем ссылки на товары в хитах продаж
href = []
goods = driver.find_elements_by_xpath('//div[@class="gallery-layout"][1]//li//h4[@itemprop="name"]/a')
for good in goods:
    href.append(good.get_attribute('href'))

# Переходим по каждой ссылке и собираем данные через запросы
for link in href:
    link_req = requests.get(link, headers=headers)
    root = html.fromstring(link_req.text)
    title = root.xpath('//h1[@class="e-h1 sel-product-title"]/text()')[0].replace('  ','').replace('\n','').replace('\r','').replace('\t','')
    cost = int(''.join(filter(lambda x: x.isdigit(), root.xpath('//div[@class = "c-pdp-price__old"]/text()')[0])))
    cost_sale = int(''.join(filter(lambda x: x.isdigit(), root.xpath('//div[@class = "c-pdp-price__current sel-product-tile-price"]/text()')[0])))
    result = {
        'title': title,
        'href': link,
        'cost': cost,
        'cost_sale': cost_sale
    }
    collection.insert_one(result)

driver.quit()

