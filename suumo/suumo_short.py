import requests as rq
import json
import codecs
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from datetime import datetime,timedelta
from pytz import timezone

import time

def FromStrToDatetime(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def FromDatetimeToStr(x):
    return x.strftime("%Y-%m-%d-%H-%M-%S")

def json_write(path,x):
    with codecs.open(path,'w','utf-8') as f:
        dump = json.dumps(x,ensure_ascii=False)
        f.write(dump)
        f.close()

def MakeDir(output_path, dir_name):
    output_dir = output_path + dir_name
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    return output_dir + "/"

def get_maxpage(soup):
    max_page = 1
    tmp = soup.find('div', attrs={'class': 'pagination pagination_set-nav'})
    pages = tmp.find('ol', attrs={'class': 'pagination-parts'})
    for p in pages.find_all('a'):
        if p.text:
            if max_page <= int(p.text):
                max_page = int(p.text)
    return max_page

def get_rooms(table):
    """
    """
    rooms = []
    for tb in table.find_all('tbody'):
        room = {'price': None, 'admin': None, 'deposit': None, 'gratuity': None,
                'floor_plan': None, 'occupied_area': None, 'floor': None, 'link': None, 'new': 0}
        for td in tb.find_all('td'):
            if td.find('ul'):
                if td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--rent'}):
                    room['price'] = td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--rent'}).text
                if td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--administration'}):
                    room['admin'] = td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--administration'}).text
                if td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--deposit'}):
                    room['deposit'] = td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--deposit'}).text
                if td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--gratuity'}):
                    room['gratuity'] = td.find('span', attrs={'class': 'cassetteitem_price cassetteitem_price--gratuity'}).text
                if td.find('span', attrs={'class': 'cassetteitem_madori'}):
                    room['floor_plan'] = td.find('span', attrs={'class': 'cassetteitem_madori'}).text
                if td.find('span', attrs={'class': 'cassetteitem_menseki'}):
                    occupied_area = td.find('span', attrs={'class': 'cassetteitem_menseki'}).text
                    room['occupied_area'] = occupied_area.replace('m2', '')
            else:
                if '階' in td.text:
                    room['floor'] = td.text.replace('\r', '').replace('\n', '').replace('\t', '')
                elif '詳細を見る' in td.text:
                    room['link'] = 'https://suumo.jp' + td.find('a').get('href')
                elif td.get('class') is not None and 'cassetteitem_other-checkbox--newarrival' in td.get('class'):
                    room['new'] = 1
        rooms.append(room)
    return rooms

def get_base_url(name, page):
    """
    """
    base = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13'
    base += '&sc=' + name
    base += '&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&pc=50&'
    base += 'page=' + str(page)
    return base

def get_reails(cassetteitems):
    """
    """
    retails = []
    for c in cassetteitems:
        
        body = c.find('div', attrs={'class': 'cassetteitem-detail-body'})
        label = body.find('div', attrs={'class': 'cassetteitem_content-label'}).text
        title = body.find('div', attrs={'class': 'cassetteitem_content-title'}).text
        address = body.find('li', attrs={'class': 'cassetteitem_detail-col1'}).text
        
        col2 = body.find('li', attrs={'class': 'cassetteitem_detail-col2'})
        stations = [p.text for p in col2.find_all('div', attrs={'class': 'cassetteitem_detail-text'})]
        
        col3 = body.find('li', attrs={'class': 'cassetteitem_detail-col3'})
        build = [p.text for p in col3.find_all('div')]
        
        table = c.find('table', attrs={'class': 'cassetteitem_other'})
            
        retail = {'label': label, 'title': title, 'address': address, 'stations': stations, 'build': build, 'rooms': get_rooms(table)}
        
        retails.append(retail)
    return retails

if('__main__' == __name__):

    ####################
    # Set params
    ####################
    output_path = "../dat/"
    url = 'https://suumo.jp/chintai/tokyo/city/'
    
    ua = UserAgent()
    header = {'User-Agent': ua.chrome}
    

    next_time = datetime.now(timezone('Asia/Tokyo'))

    while(True):
        now = datetime.now(timezone('Asia/Tokyo')) 
        if(now >= next_time):            
            timestamp = str(int(now.timestamp()))
            
            r = rq.get(url, headers=header)
            soup = BeautifulSoup(r.text, 'lxml')
            
            targets = {}
            
            city_body = soup.find_all('ul', attrs={"class", "searchitem-list"})
            for city in city_body:
                for site in city.find_all('li'):
                    if site.find('input').get('id'):
                        name = site.find('span').text
                        rid = site.find('input').get('id').replace('la', '')
                        targets[name] = rid
            
            for name in targets:
                
                city_num = targets[name]
                base = get_base_url(targets[name], 1)
                r = rq.get(base, headers=header)
                
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'lxml')
                    
                    max_page = get_maxpage(soup)
                    
                    cassetteitems = soup.find_all('div', attrs={'class': 'cassetteitem'})

                    retails = []
                    retails += get_reails(cassetteitems)
                    
                    if max_page == 1:
                        pass
                    else:
                        for page in range(2,max_page+1):
                            base = get_base_url(city_num, page)
                            r = rq.get(base, headers=header)
                            soup = BeautifulSoup(r.text, 'lxml')
                            
                            cassetteitems = soup.find_all('div', attrs={'class': 'cassetteitem'})
                            retails += get_reails(cassetteitems)            
                            time.sleep(5)
                
                    root_dir = MakeDir(output_path, now.strftime("%Y%m%d"))
                    output_dir = MakeDir(root_dir, city_num)
                    fname = "T" + timestamp + ".json"
                    output_fpath = output_dir + fname
                    
                    json_write(output_fpath, retails)
                else:
                    pass
            next_time += timedelta(hours = 6)
        else:
            time.sleep(600)