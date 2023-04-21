from setting import ENGINE, Base  
from create_inputs import Inputs
from create_outputs import Outputs
from sqlalchemy.orm import sessionmaker

import glob
from decimal import Decimal

import codecs
import json
from datetime import datetime

def json_load(path):
    with codecs.open(path,'r','utf-8') as f:
        return json.loads(f.read())

def json_write(path,x):
    with codecs.open(path,'w','utf-8') as f:
        dump = json.dumps(x,ensure_ascii=False)
        f.write(dump)
        f.close()

def get_addr_info(date, height, tmp_json):
    inputs = []
    outputs = []
    err_txs = []
    for i,txs in enumerate(tmp_json):
        try:
            h = txs['hash']
            idx = str(txs['id'])
            if 'Generation + Fees' in txs['inputs']:
                inputs.append({'date': date, 'height': height, 
                                'addr': 'Generation + Fees', 'h': txs['hash'],
                                'v': txs['v'], 'w': None})
            else:
                tmp_inputs = {}
                for j,tmp_addr in enumerate(txs['inputs']):
                    if tmp_addr['a'] in tmp_inputs:
                        tmp_inputs[tmp_addr['a']]['v'] += Decimal(str(tmp_addr['v']))
                    else:
                        tmp_inputs[tmp_addr['a']] = {'v': Decimal(str(tmp_addr['v']))}
                        if 'w' in tmp_addr:
                            tmp_inputs[tmp_addr['a']]['w'] = tmp_addr['w']
                
                for addr in tmp_inputs:
                    if 'w' in tmp_inputs[addr]:
                        inputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                        'v': tmp_inputs[addr]['v'], 'w': tmp_inputs[addr]['w']})
                    else:
                        inputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                        'v': tmp_inputs[addr]['v'], 'w': None})   
            tmp_outputs = {}
            for j,tmp_addr in enumerate(txs['outputs']):
                if tmp_addr['a'] in tmp_outputs:
                    tmp_outputs[tmp_addr['a']]['v'] += Decimal(str(tmp_addr['v']))
                else:
                    tmp_outputs[tmp_addr['a']] = {'v': Decimal(str(tmp_addr['v']))}
                    if 'w' in tmp_addr:
                        tmp_outputs[tmp_addr['a']]['w'] = tmp_addr['w']
        
            for addr in tmp_outputs:
                if 'w' in tmp_outputs[addr]:
                    outputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                    'v': tmp_outputs[addr]['v'], 'w': tmp_outputs[addr]['w']})
                else:
                    outputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                    'v': tmp_outputs[addr]['v'], 'w': None}) 
        except:
            err_txs.append(txs)
    return inputs, outputs, err_txs

if '__main__' == __name__:

    dirs = glob.glob('../../tx/block_hash_2*')
    dirs.sort()

    fin_txs = json_load('./log/fin_txs.json')
    current_tx = json_load('./log/current_tx.json')

    for dpath in dirs:
        if dpath in fin_txs:
            pass
        else:
            files = glob.glob(dpath + '/*')
            files.sort()
   
            for f in files:
                height = f.split('/')[-1].replace('.json', '')

                if current_tx[0] >= int(height):
                    pass
                else:

                    tmp_json = json_load(f)

                    Session = sessionmaker(bind=ENGINE)
                    session = Session()
                    sql = "select time from block_statistics where height = " + height
                    res = session.execute(sql)
                    session.close()

                    for v in res: 
                        date = datetime.strftime(v.time, '%Y%m%d')

                    inputs, outputs, err_txs = get_addr_info(date, int(height), tmp_json)

                    if err_txs:
                        json_write('./err/' + height + '.json', err_txs)

                    # insert inputs
                    Session = sessionmaker(bind=ENGINE)  
                    session = Session()
                    flag=False
                    for i, idx in enumerate(inputs):
                        item = Inputs(idx)
                        session.add(item)
                        if i%1000 == 0:
                            session.commit()
                            flag=False
                        else:
                            flag=True
                    if flag:
                        session.commit()
                    session.close()

                    # insert outputs
                    Session = sessionmaker(bind=ENGINE)  
                    session = Session()
                    flag=False
                    for i, idx in enumerate(outputs):
                        item = Outputs(idx)
                        session.add(item)
                        if i%1000 == 0:
                            session.commit()
                            flag=False
                        else:
                            flag=True
                    if flag:
                        session.commit()
                    session.close()

                    json_write('./log/current_tx.json', [int(height)])

            fin_txs.append(dpath)
            json_write('./log/fin_txs.json', fin_txs)

