#           Урок 3. Парсинг HTML. BS, SQLAlchemy

#1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД
#2) Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введенной суммы
#3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

from pymongo import MongoClient
from pprint import pprint
import pandas as pd
from sod_hw_2_1 import hh_parce
from sod_hw_2_1 import sj_parce

client = MongoClient('localhost',27017)
vacansies_db = client['vacansies_db']
hh_sj_col = vacansies_db['hh_sj_col']

query_text = 'программист'
num_pages = 1
headers =  {'accept':'*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
base_url_hh = f'https://hh.ru/search/vacancy?area=1&search_period=3&text={query_text}'
base_url_sj = f'https://www.superjob.ru/vacancy/search/?keywords={query_text}&geo%5Bt%5D%5B0%5D=4'


# Загрузить данные из файла в коллекцию. При этом вызываются функции сбора данных с сайтов
def load_to_base(collection, base_url_hh, base_url_sj, headers, num_pages):
    jobs = hh_parce(base_url_hh, headers, num_pages)
    jobs_sj = sj_parce(base_url_sj, headers, num_pages)
    jobs = jobs.append(jobs_sj, ignore_index=True)
    try:
        #collection.insert_many(pd.read_csv(source_addr).to_dict('records'))
        collection.insert_many(jobs.to_dict('records'))
    except:
        print('Ошибка при загрузке данных')


# Удаление всех данных из коллекции
def delete_all(collection):
    collection.delete_many({})


# Вывод всех данных коллекции
def print_all(collection):
    objects = collection.find()
    for obj in objects:
        pprint(obj)


# Вывод всех записей с ЗП, большей, чем задано
def print_compens_more_then(val, collection):
    objects = collection.find({'compensation1': {'$gt': val}}, {'company', 'compensation1'})
    for obj in objects:
        pprint(obj)


# Вывод количества записей в коллекции
def print_collect_len(collection):
    print(collection.count_documents({}))


# Добавить новые вакансии
def add_new_vac(collection, base_url_hh, base_url_sj, headers, num_pages):
    jobs = hh_parce(base_url_hh, headers, num_pages)
    jobs_sj = sj_parce(base_url_sj, headers, num_pages)
    jobs = jobs.append(jobs_sj, ignore_index=True)
    try:
        new_dict = jobs.to_dict('records')
    except:
        print('Ошибка при загрузке данных')
        return
    new_record_cnt = 0
    for item in new_dict:
        record = collection.find_one({'href':item['href']})
        if not record:
            new_record_cnt += 1
            collection.insert_one(item)
            print(item)
    print(f'Всего добавлено {new_record_cnt} записей')

# Обновить вакансии
def update_vac(collection, base_url_hh, base_url_sj, headers, num_pages):
    jobs = hh_parce(base_url_hh, headers, num_pages)
    jobs_sj = sj_parce(base_url_sj, headers, num_pages)
    jobs = jobs.append(jobs_sj, ignore_index=True)
    try:
        new_dict = jobs.to_dict('records')
    except:
        print('Ошибка при загрузке данных')
        return
    for item in new_dict:
        collection.update_one(
            {'href':'item["href"]'},
            {'$set':item},
        )


print_collect_len(hh_sj_col)
delete_all(hh_sj_col)
#load_to_base(hh_sj_col, base_url_hh, base_url_sj, headers, num_pages)
#update_vac(hh_sj_col, base_url_hh, base_url_sj, headers, num_pages)
#print_all(hh_sj_col)
#add_new_vac(hh_sj_col, base_url_hh, base_url_sj, headers, num_pages)
print_collect_len(hh_sj_col)
#print_compens_more_then(100000, hh_sj_col)


