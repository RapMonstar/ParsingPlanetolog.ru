'''Зайдите на следующую страницу planetolog.ru (или любого подобного) и спарсите ссылки на все страны мира,
зайдите в каждую страну, спарсите ее города, зайдите в каждый город и спарсите описание этого города.
'''

import requests
from bs4 import BeautifulSoup
import csv

HOST = 'http://planetolog.ru/'
URL = 'http://planetolog.ru/country-list.php'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_countries(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('td', class_='CountryList')
    cards = {}

    for item in items:
        for country in item.find_all('a', href=True):
            cards[country.text] = {'link': HOST + country.get('href')}

    return cards


def get_cities(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='textplane')

    for item in items:
        for city in item.find_all('a', href=True):
            if city.text[:6] == "Города":
                return HOST + city.get('href')


def get_every_cities(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('td', class_='CountryList')
    cards = {}
    for item in items:
        for every_city in item.find_all('a', href=True):
            if every_city == None:
                continue

            cards[every_city.text] = {'link': HOST + every_city.get('href')}

    return cards


def get_attractions(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='textplane')
    res = ''
    for item in items:
        #print('-------------------------------------------------------------------------------')

        for attractions in item.find_all('p'):
            #print(attractions)
            res += str(attractions)

    res = res.replace('<p>', '')
    res = res.replace('</p>', '')
    res = res.replace('<br/>', '')
    res = res.replace('\r\n', ' ')
    res = res.strip()
    return res

if __name__ == '__main__':
    html = get_html(URL)
    result = get_countries(html.text)
    i = 0
    attraction = {}
    for k, r in result.items():
        if i == -1:
            break

        r['citylink'] = get_cities(get_html(r['link']).text)
        print(r)
        if r['citylink'] == None:
            #print(r)
            continue
        else:
            r['cities'] = get_every_cities(get_html(r['citylink']).text)
            #print(r['city'])
            i += 1
            for a in r['cities']:

                r['cities'][a]['attraction'] = get_attractions(get_html(r['cities'][a]['link']).text)

                #print(get_html(r['city'][a]['city']).text)

    print(result)
    f = open('text.txt', 'w')
    f.write(str(result))
# print(get_attractions(get_html(URL)).text
