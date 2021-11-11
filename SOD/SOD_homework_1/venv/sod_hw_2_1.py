#               Урок 2. Парсинг HTML. BeautifulSoup, MongoDB
#1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через
# input или аргументы). Получившийся список должен содержать в себе минимум:
#    *Наименование вакансии
#    *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#    *Ссылку на саму вакансию
#    *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение.
# Данная структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с
# помощью dataFrame через pandas.




from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import time
import numpy as np
import string
from pymongo import MongoClient



def hh_parce(base_url, headers, pages):
    # Чтобы сайт думал, что с этого браузера зашел один пользователь для просмотра вакансий
    jobs = []
    session = requests.Session()
    for i in range(pages):
        request = session.get(base_url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            # Т.к. есть два типа объявлений: премиум и обычные
            divs = soup.find_all('div', {'data-qa':['vacancy-serp__vacancy vacancy-serp__vacancy_premium', 'vacancy-serp__vacancy']})
            for div in divs:
                title = div.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
                href = div.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
                company = div.find('a', {'data-qa':'vacancy-serp__vacancy-employer'})
                if not company:
                    company = np.nan
                else:
                    company = company.text
                compensation = div.find('div', {'data-qa': 'vacancy-serp__vacancy-compensation'})

                if not compensation:
                    compensation1 = np.nan
                    compensation2 = np.nan
                    money_type = np.nan
                else:
                    compensation = compensation.text.replace('.','')
                    money_type = compensation[-3:].lower()


                    if '-' in compensation:
                        compensation1 = compensation.split('-')[0]
                        compensation2 = compensation.split('-')[1]
                        compensation1 = ''.join(filter(lambda x: x.isdigit(), compensation1))
                        compensation2 = ''.join(filter(lambda x: x.isdigit(), compensation2))
                    elif 'от' in compensation:
                        #compensation1 = compensation.replace('от ','')
                        compensation1 = ''.join(filter(lambda x: x.isdigit(), compensation))
                        compensation2 = np.nan
                    elif 'до' in compensation:
                        compensation1 = np.nan
                        #compensation2 = compensation.replace('до ','')
                        compensation2 = ''.join(filter(lambda x: x.isdigit(), compensation))

                #print(compensation1, end='\t')
                #print(compensation2)
                #print(money_type)
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'compensation1': compensation1,
                    'compensation2': compensation2,
                    'money_type': money_type,
                    'source':'hh.ru'
                })
            # Если следующей страницы нет, ты выход из цикла
            base_url = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
            if not base_url:
                brake
            else:
                base_url = 'https://hh.ru' + base_url['href']
            time.sleep(1)
        else:
            brake

    jobs = pd.DataFrame(jobs)
    return jobs



def sj_parce(base_url, headers, pages):
    # Чтобы сайт думал, что с этого браузера зашел один пользователь для просмотра вакансий
    jobs = []
    session = requests.Session()
    for i in range(pages):
        request = session.get(base_url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', {'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
            for div in divs:
                title = div.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).text
                href = div.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).findParent()['href']
                # В одном месте нет названия фирмы
                company = div.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'})
                if not company:
                    company = np.nan
                else:
                    company = company.getText()
                #print(company)
                compensation = div.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).text
                #compensation = compensation.replace(' ', '')

                # Так как везде, где указана зп, она указана в рублях
                money_type = 'руб'


                if '—' in compensation:
                    compensation1 = compensation.split('—')[0]
                    compensation2 = compensation.split('—')[1]
                    compensation1 = ''.join(filter(lambda x: x.isdigit(), compensation1))
                    compensation2 = ''.join(filter(lambda x: x.isdigit(), compensation2))

                elif 'от' in compensation:
                    #compensation1 = compensation[3:]
                    compensation1 = ''.join(filter(lambda x: x.isdigit(), compensation))
                    compensation2 = np.nan
                elif 'договорённости' in compensation:
                    compensation1 = np.nan
                    compensation2 = np.nan
                    money_type = np.nan

                elif 'до' in compensation:
                    compensation1 = np.nan
                    #compensation2 = compensation[3:]
                    compensation2 = ''.join(filter(lambda x: x.isdigit(), compensation))

                # Если одно значение без от и до
                else:
                    compensation1 = ''.join(filter(lambda x: x.isdigit(), compensation))
                    compensation2 = np.nan

                #print(compensation1, end='\t')
                #print(compensation2)
                #print(compensation)
                #print(money_type)
                jobs.append({
                    'title': title,
                    'href': 'https://www.superjob.ru'+href,
                    'company': company,
                    'compensation1': compensation1,
                    'compensation2': compensation2,
                    'money_type': money_type,
                    'source': 'superjob.ru'
                })

            # Если следующей страницы нет, ты выход из цикла
            base_url = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})
            if not base_url:
                brake
            else:
                base_url = 'https://www.superjob.ru' + base_url['href']
            time.sleep(1)
        else:
            brake
    jobs = pd.DataFrame(jobs)
    return jobs

query_text = 'программист'
num_pages = 3
headers =  {'accept':'*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
base_url_hh = f'https://hh.ru/search/vacancy?area=1&search_period=3&text={query_text}'
base_url_sj = f'https://www.superjob.ru/vacancy/search/?keywords={query_text}&geo%5Bt%5D%5B0%5D=4'

jobs = hh_parce(base_url_hh, headers, num_pages)
#jobs.to_csv('hh.csv')
jobs_sj = sj_parce(base_url_sj, headers, num_pages)
#jobs_sj.to_csv('sj.csv')
jobs = jobs.append(jobs_sj, ignore_index=True)
jobs.to_csv('hh+sj.csv')

#print(jobs.to_dict())

