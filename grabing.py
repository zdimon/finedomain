#!/usr/bin/env python
# -*- coding: utf-8 -*-
print('Start')
import requests
from bs4 import BeautifulSoup
import json
import time
data = []




def check_domain(domain):
    url = 'https://zen.yandex.com/%s' % domain
    try:
        r = requests.get(url)
        if r.status_code == 404:
            return False
        else:
            return True
    except:
        print('Fatal error')
        return False

#check_domain('ssssabai.tv')

with open('data.json','r') as f:
    out = f.read()
    out = json.loads(out)
    count = len(out)
    print(count)
    for item in out:
        count = count - 1
        rezult = check_domain(item['domain'])
        if rezult:
            with open('success.txt', 'a') as of:
                of.write(item['domain']+';')
        print('Domain %s result %s' % (item['domain'], rezult))
        print(count)






def check_end(soup):

    try:
        h2 = soup.find("h2")
        if h2.text.encode('utf-8').find('отвечающих заданным критериям')>0:
            return True
        else:
            return False
    except:
        return False





pages = range(0,800)



for page in pages:
    url = 'https://www.reg.ru/domain/deleted/?&free_from=07.06.2019&free_to=07.06.2019&order=ASC&sort_field=dname_idn%20%20%20%20&page=%s' % page
    print("loading .. %s" % page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    if not check_end(soup):
        table = soup.find("table",{"class": "b-table__content"})
        tbody = table.find("tbody")
        trs = tbody.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            data.append({"domain": tds[0].text, "date_expire": tds[2].text})
    else:
        print('End pages')
        break
    time.sleep(30)

print("Saving into the file data.json")
f = open('data.json','w')
f.write(json.dumps(data))
f.close()
#print(data)


