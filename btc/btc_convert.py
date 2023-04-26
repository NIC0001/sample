
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
                                'v': str(txs['v']), 'w': ''})
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
                                        'v': str(tmp_inputs[addr]['v']), 'w': str(tmp_inputs[addr]['w'])})
                    else:
                        inputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                        'v': str(tmp_inputs[addr]['v']), 'w': ''})   
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
                                    'v': str(tmp_outputs[addr]['v']), 'w': str(tmp_outputs[addr]['w'])})
                else:
                    outputs.append({'date': date, 'height': height, 'addr': addr, 'h': txs['hash'],
                                    'v': str(tmp_outputs[addr]['v']), 'w': ''}) 
        except:
            err_txs.append(txs)
    return inputs, outputs, err_txs

current_tx = [0]

fw_in = codecs.open('./in_' + target + '.csv', 'w', encoding='utf-8')
fw_in.write('date,height,hash,address,v,w\n')
fw_out = codecs.open('./out_' + target + '.csv', 'w', encoding='utf-8')
fw_out.write('date,height,hash,address,v,w\n')

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

        for tx in inputs:
            fw_in.write('%s,%s,%s,%s,%s,%s\n' % (tx['date'], tx['height'], tx['h'],
                                                 tx['addr'], tx['v'], tx['w']))

        for tx in outputs:
            fw_out.write('%s,%s,%s,%s,%s,%s\n' % (tx['date'], tx['height'], tx['h'],
                                                 tx['addr'], tx['v'], tx['w']))

        if err_txs:
            json_write('./err/' + height + '.json', err_txs)
fw_in.close()
fw_out.close()

