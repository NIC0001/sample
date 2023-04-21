import requests as rq
import json
import codecs
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

from datetime import datetime,timedelta
from pytz import timezone

import time


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
    max_page = re.search('pg=\d+', soup.find('li', attrs={"class", "m_pager_l_last"}).find('a').get('href')).group()
    return max_page.replace('pg=', '')

def get_rooms(items):
    rooms = []
    
    for i in items:
        room = {'floor': i.find('div', attrs={'class': 'm_prpty_item_floor'}).text.replace('\n', ''),
                'price': i.find('span', attrs={'class': 'm_prptydata_mon'}).text,
                'admin': i.find('li', attrs={'class': 'm_prptydata_submon'}).text,
                'deposit': i.find('span', attrs={'class': 'm_tag_deposit'}).text,
                'link': i.find('a', attrs={'class': 'm_prpty_item_linkarea_btn kpi_click'}).get('href')
               }
        
        additional = i.find_all('ul', attrs={'class': 'm_prptydata_list m_prptydata_data_s'})
        
        tmp = []
        for a in additional:
            for l in a.find_all('li'):
                if '敷' in l.text:
                    room['deposit'] = l.text
                elif '礼' in l.text:
                    room['gratuity'] = l.text
                elif 'm²' in l.text:
                    room['occupied_area'] = l.text
                else:
                    if l.text is not None and l.text != '':
                        tmp.append(l.text)
        room['others'] = tmp
                
        rooms.append(room)
        
    return rooms

def get_base_url(name, page):
    base = 'https://www.homemate.co.jp/pr-tokyo/'
    base += name
    base += '/?pg=' + str(page)
    base += '&so=17'
    return base

def get_reails(propties):
    retails = []
    for p in propties:
        title = p.find('div', attrs={'class': 'm_prpty_maininfo_name'}).text
        info = list(p.find('p', attrs={'class': 'm_prpty_maininfo_txt'}).children)
        p_data = p.find('div', attrs={'class': 'm_prpty_maininfo_data'})
        build = [p.text for p in p_data.find_all('li')]
        items = p.find_all('div', attrs={'class': 'm_prpty_item js_formcheckarea'})
            
        retail = {'title': title, 'info': info, 'build': build, 'build': build, 'rooms': get_rooms(items)}
        
        retails.append(retail)
        
    return retails

if('__main__' == __name__):

    ####################
    # Set params
    ####################
    output_path = "../dat/"
    url = 'https://www.homemate.co.jp/pr-tokyo/city/'
    
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
            city_body = soup.find('table', attrs={"class", "m_table_form js_floatingmenu_formarea"})
            for l in city_body.find_all('li'):
                c = l.find('input', attrs={"class", "m_input_check_smallregion m_input_check m_input_check_spblock js_all_item js_url_input_param"})
                if c.get('disabled') is None:
                    targets[l.find('a').text] = c.get('value')
            
            for name in targets:
                
                city_num = targets[name]
                base = get_base_url(targets[name], 1)
                r = rq.get(base, headers=header)
                
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'lxml')
                    
                    max_page = get_maxpage(soup)
                    max_page = int(max_page)
                    
                    propties = soup.find_all('section', attrs={"class", "m_prpty_box"})

                    retails = []
                    retails += get_reails(propties)

                    if max_page == 1:
                        pass
                    else:
                        for page in range(2, max_page+1):
                            base = get_base_url(targets[name], page)
                            r = rq.get(base, headers=header)
                            soup = BeautifulSoup(r.text, 'lxml')
                            
                            propties = soup.find_all('section', attrs={"class", "m_prpty_box"})
                            retails += get_reails(propties)            
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