import requests as rq
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import codecs
import json
import sys
import glob
import os


def json_write(path,x):
    with codecs.open(path,'w','utf-8') as f:
        dump = json.dumps(x,ensure_ascii=False)
        f.write(dump)
        f.close()


if __name__ == '__main__':

    links = glob.glob('../dat/*')
    ua = UserAgent()
    header = {'User-Agent': ua.chrome}
    

    for idx,link in enumerate(links):
        sys.stdout.write("\r %d / %d" % (idx+1, len(links)))
        sys.stdout.flush()
        
        fname = link.split('/')[-2] + link.split('/')[-1].replace('?bc', '_bc')
        
        if os.path.isfile('../dat/20230221/' + fname + '.json'):
            pass
        else:
            r = rq.get('https://suumo.jp/' + link, headers=header)
            
            if r.status_code == 200:        
                soup = BeautifulSoup(r.text, 'lxml')
                
                retail_data = {} 
                retail_data['name'] = soup.find('h1', attrs={'class': 'section_h1-header-title'}).text

                property_body = soup.find('div', attrs={'class': 'property_view_note-info'})
                property_list = property_body.find_all('div', attrs={'class': 'property_view_note-list'})

                retail_data['rent'] = property_list[0].find_all('span')[0].text
                retail_data['mange_comm_fee'] = property_list[0].find_all('span')[1].text

                for p in property_list[1].find_all('span'):
                    if '敷金' in p.text:
                        retail_data['dep'] = p.text
                    elif '礼金' in p.text:
                        retail_data['gratuity'] = p.text
                    elif '保証金' in p.text:
                        retail_data['guarantee'] = p.text        
                    elif '敷引・償却' in p.text:
                        retail_data['dep_amort'] = p.text    

                image_links = soup.find('ul', attrs={'class': 'l-property_view_thumbnail'})

                retail_data['image_links'] = []
                if image_links is not None:
                    for i in image_links.find_all('li'):
                        retail_data['image_links'].append(i.find('img').get('data-src'))
                    
                property_body = soup.find('div', attrs={'class': 'l-property_view_table'})
                property_table = property_body.find('table', attrs={'class': 'property_view_table'})
                for p in property_table.find_all('tr'):
                    for j,q in enumerate(p.find_all('th')):
                        if '所在地' in q.text:
                            retail_data['address'] = p.find_all('td')[j].text
                        elif '駅徒歩' in q.text:
                            retail_data['walk_station'] = p.find_all('td')[j].text
                        elif '間取り' in q.text:
                            retail_data['floor_plan'] = p.find_all('td')[j].text
                        elif '築年数' in q.text:
                            retail_data['built'] = p.find_all('td')[j].text
                        elif '向き' in q.text:
                            retail_data['window'] = p.find_all('td')[j].text
                        elif '専有面積' in q.text:
                            retail_data['occupied_area'] = p.find_all('td')[j].text
                        elif '階' in q.text:
                            retail_data['floor'] = p.find_all('td')[j].text
                        elif '建物種別' in q.text:
                            retail_data['building_class'] = p.find_all('td')[j].text
                
                if soup.find('div', attrs={'id': 'bkdt-option'}) is not None:
                    inline_list = soup.find('div', attrs={'id': 'bkdt-option'})
                    inline_list = inline_list.find('ul', attrs={'class': 'inline_list'})
                    retail_data['inline_list'] = inline_list.find('li').text
                else:
                    retail_data['inline_list'] = ''

                table_gaiyou = soup.find('table', attrs={'class': 'data_table table_gaiyou'})
                for p in table_gaiyou.find_all('tr'):
                    for j,q in enumerate(p.find_all('th')):
                        if '間取り詳細' in q.text:
                            retail_data['floor_plan_d'] = p.find_all('td')[j].text
                        elif '構造' in q.text:
                            retail_data['structure'] = p.find_all('td')[j].text
                        elif '階建' in q.text:
                            retail_data['story'] = p.find_all('td')[j].text
                        elif '築年月' in q.text:
                            retail_data['Building_date'] = p.find_all('td')[j].text
                        elif '損保' in q.text:
                            retail_data['insurance'] = p.find_all('td')[j].text
                        elif '駐車場' in q.text:
                            retail_data['parking'] = p.find_all('td')[j].text
                        elif '入居' in q.text:
                            retail_data['moving_in'] = p.find_all('td')[j].text
                        elif '取引態様' in q.text:
                            retail_data['transactions'] = p.find_all('td')[j].text
                        elif '条件' in q.text:
                            retail_data['conditions'] = p.find_all('td')[j].text
                        elif '取り扱い店舗' in q.text:
                            retail_data['property_code'] = p.find_all('td')[j].text
                        elif 'SUUMO' in q.text:
                            retail_data['suumo_code'] = p.find_all('td')[j].text
                        elif '総戸数' in q.text:
                            retail_data['total_units'] = p.find_all('td')[j].text
                        elif '情報更新日' in q.text:
                            retail_data['update'] = p.find_all('td')[j].text            
                        elif '次回更新日' in q.text:
                            retail_data['next_update'] = p.find_all('td')[j].text                   
                        elif '保証会社' in q.text:
                            retail_data['insurance_company'] = p.find_all('td')[j].text                
                        elif 'ほか初期費用' in q.text:
                            retail_data['other_initial_costs'] = p.find_all('td')[j].text          
                        elif 'ほか諸費用' in q.text:
                            retail_data['other_expenses'] = p.find_all('td')[j].text                   
                        elif '備考' in q.text:
                            retail_data['note'] = p.find_all('td')[j].text

                r = rq.get('https://suumo.jp/' + link.replace('/?bc=', '/kankyo/?bc='), headers=header)
                soup = BeautifulSoup(r.text, 'lxml')

                if soup.find('script', attrs={'type': 'application/json'}) is None:
                    retail_data['lat_lng'] = {}
                else:
                    retail_data['lat_lng'] = json.loads(soup.find('script', attrs={'type': 'application/json'}).text)
                
                json_write('../dat/20230221/' + fname + '.json', retail_data)
                time.sleep(1)