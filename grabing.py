#!/usr/bin/env python
# -*- coding: utf-8 -*-
# импортируем все что надо для работы
import requests
from bs4 import BeautifulSoup
import json
import time
import sys
# начало программы
print('Начинаем грабить домены.')
print("Вводи за какую дату? (типа 12.06.2019):   ")
user_date = raw_input()
print("Работаем по {}".format(user_date))

def save_success(domain):
    with open('success.txt', 'a+') as of: # открываем для добавления и создаем если нет
        of.write(domain+';')
        print('Domain %s result %s' % (domain, 'SUCCESS'))

def check_domain(domain):
    # формирую url, адрес подставляя домен в строку
    url = 'https://zen.yandex.com/%s' % domain
    # пробую сделать запрос
    try:
        # получаю страницу
        r = requests.get(url)
        if r.status_code == 404: # проверяю статус
            print('Domain %s result %s' % (domain, 'FAIL!'))
            return False
        else:
            print('Domain %s result %s' % (domain, 'SUCCESS'))
            # если повезло и домен нашли
            return True
    except KeyboardInterrupt: # выход по ctrl+c
        print("Ну пока!")
        sys.exit() # нагло вываливаемся из проги
    # это если запрос обрушился по какой то причине        
    except:
        print('Request error %s' % url)
        return False

def check_end(soup):
    ''' Определяю конец постранички '''
    try:
        # на конечной странице был замечен заголовок h1 с текстом
        '''
                Доменов, отвечающих заданным критериям фильтрации, не&nbsp;найдено. 
        '''
        h2 = soup.find("h2")
        # тут для поиска сказало что нужно вначале кодировать в UTF-8
        if h2.text.encode('utf-8').find('отвечающих заданным критериям')>0:
            return True
        else:
            return False
    except:
        return False

is_end = False
page = 0
while not is_end:
    # определяю строку с урлом
    # к ней с конца буду прилеплять страницы 
    url = 'https://www.reg.ru/domain/deleted/?&free_from=%s&free_to=%s&order=ASC&sort_field=dname_idn%20%20%20%20&page=%s' % (user_date,user_date,page)
    print("Делаю страницу %s" % page)
    # добавляем счетчик страниц
    page = page + 1

    # запрос первой страницы
    r = requests.get(url)

    # тут буду хранить домены
    data = []

    # парсим html
    soup = BeautifulSoup(r.text, 'html.parser')

    # проверим конец постранички
    if check_end(soup):
        is_end = True
        break # ломаем цикл
        

    # находим первую таблицу по тегу и css классу
    table = soup.find("table",{"class": "b-table__content"})

    # в ней блок tbody по имени тега
    tbody = table.find("tbody")

    # строки
    trs = tbody.findAll("tr")
    for tr in trs:
        # ячейки
        tds = tr.findAll("td")
        # добавляем домен и срок истечения в список
        data.append({"domain": tds[0].text, "date_expire": tds[2].text})
        # проверяю домен на zen.yandex.com
        if check_domain(tds[0].text):
            save_success(tds[0].text)

print('The end')