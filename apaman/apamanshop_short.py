import requests as rq
import json
import codecs
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from datetime import datetime,timedelta
from pytz import timezone

import time
import re

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

def get_targets(soup):
    city_body = soup.find('table', attrs={"class", "form_table"})
    targets = {}

    for l in city_body.find_all('li', attrs={"class", "mod_check"}):
        c = l.find('a')
        targets[c.text] = c.get('href')
    return targets

def get_maxpage(soup):
    pages = soup.find('ul', attrs={"class", "mod_pager"})

    max_page = 0
    for a in pages.find_all('a'):
        if re.search('page=\d+', a.get('href')):
            tmp_page = re.search('page=\d+', a.get('href')).group()
            tmp_page = tmp_page.replace('page=', '')
            
            if max_page <= int(tmp_page):
                max_page = int(tmp_page)
                
    return max_page

def get_room(room_list):
    rooms = []
    for r in room_list.find_all('tr', attrs={"class", "tr_mid"}):
        room = {}
        tds = r.find_all('td')
        room['floor'] = tds[1].find('p').text
        room['price'] = tds[2].find_all('p')[0].text
        room['admin'] = tds[2].find_all('p')[1].text
        
        if len(tds[3].find_all('p')) == 1:
            room['deposit'] = tds[3].find_all('p')[0].text
            room['gratuity'] = tds[3].find_all('p')[0].text
        else:
            room['deposit'] = tds[3].find_all('p')[0].text
            room['gratuity'] = tds[3].find_all('p')[1].text
        room['floor_plan'] = tds[4].find_all('p')[0].text
        room['occupied_area'] = tds[4].find_all('p')[1].text.replace('m²', '')
        room['link'] = 'https://www.apamanshop.com' + tds[6].find('p', attrs={"class", "dp_inb v_m"}).find('a').get('href')
        rooms.append(room)
        
    return rooms

def get_base_url(name, page):
    base = 'https://www.apamanshop.com'
    base += name
    base += '?page=' + str(page)
    base += '&sort_type=sort1'
    return base

def get_reails(soup):
    retails = []
    for art in soup.find_all('article', attrs={"class", "mod_box_section_bdt"}):
        retail = {}
        if 'pr' in art.get('class'):
            pass
        else:
            body = art.find('div', attrs={"class", "box_info"})
            retail['name'] = body.find('h2', attrs={"class", "name"}).text
            
            retail['build_info'] = [p.text for p in body.find('p', attrs={"class", "info"}).find_all('span')]
            retail['address'] = body.find('p', attrs={"class", "address"}).text
            retail['stations'] = [p.text.replace('\xa0', ' ') for p in body.find('ul', attrs={"class", "list_info"}).find_all('li')]
            
            retail['link'] = body.find('h2', attrs={"class", "name"}).text
            
            room_list = art.find('table', attrs={"class", "mod_table mod_table_col mod_tab2"})
            retail['rooms'] = get_room(room_list)
            retails.append(retail)
            
    return retails

if('__main__' == __name__):

    ####################
    # Set params
    ####################
    output_path = "../dat/"

    url = 'https://www.apamanshop.com/tokyo/chiiki/'
    ua = UserAgent()
    header = {'User-Agent': ua.chrome}
    

    next_time = datetime.now(timezone('Asia/Tokyo'))

    while(True):
        now = datetime.now(timezone('Asia/Tokyo')) 
        if(now >= next_time):            
            timestamp = str(int(now.timestamp()))
            
            r = rq.get(url, headers=header)
            soup = BeautifulSoup(r.text, 'lxml')
            
            targets = get_targets(soup)
            
            for name in targets:
                
                city_num = targets[name]
                base = get_base_url(targets[name], 1)
                r = rq.get(base, headers=header)
                
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'lxml')
                    
                    max_page = get_maxpage(soup)
                    
                    retails = []
                    retails += get_reails(soup)
                    
                    if max_page == 1:
                        pass
                    else:
                        for page in range(2,max_page+1):
                            base = get_base_url(city_num, page)
                            r = rq.get(base, headers=header)
                            soup = BeautifulSoup(r.text, 'lxml')
                            
                            retails += get_reails(soup)           
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