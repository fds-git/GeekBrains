# Установить selenium
# pip install selenium
# Загрузить web-драйвер для браузера

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#import time


chrome_optinons = Options()
# На всю страницу
# chrome_optinons.add_argument('start-maximized')
# Запуск без графического интерфейса (браузера)
chrome_optinons.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_optinons)
driver.get('https://lenta.com/catalog/frukty-i-ovoshchi/')
assert 'Фрукты и овощи' in driver.title

# Закрываем всплывающее окно
button = driver.find_element_by_class_name('popup__close')
button.click()
print('Закрыли окно с выбором города')
# time.sleep(2)
pages = 1
while True:
    try:
        print(f'Открыли {pages} страницу')
        #button = driver.find_element_by_class_name('catalog__pagination-button')
        button = WebDriverWait(driver, 10).until(
            #ec.presence_of_element_located((By.CLASS_NAME, 'catalog__pagination-button'))
            ec.element_to_be_clickable((By.CLASS_NAME, 'catalog__pagination-button'))
        )
        button.click()
        pages += 1
        # time.sleep(1)
    except Exception as e:
        print(e)
        print(f'Конец. Обработано {pages} страниц')
        break

goods = driver.find_elements_by_class_name('sku-card-small')
for good in goods:
    print(good.find_element_by_class_name('sku-card-small__title').text)
    print(float(good.find_element_by_class_name('price__primary--small').text.replace(',','.')))
#driver.quit()

driver.quit()