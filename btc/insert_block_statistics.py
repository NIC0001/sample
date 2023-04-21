from setting import ENGINE, Base  
from block_statistics import BlockStatistics
from sqlalchemy.orm import sessionmaker

import glob
import pandas as pd
from decimal import Decimal

if '__main__' == __name__:

    files = []
    for num in range(2022, 2023):
        files += glob.glob('../../blocks/' + str(num) + '/*')
    files.sort()

    skip_date = 20221222
    for f in files:
        date = f.split('/')[-1].split('_')[-1].replace('.tsv', '')
        if skip_date < int(date):
            print(f)
            df = pd.read_csv(f, sep='\t', dtype={'version_hex': str, 'version_bits': str, 'difficulty': str,
                                                 'chainwork': str, 'coinbase_data_hex': str,
                                                 'input_total_usd': str, 'output_total_usd': str,
                                                 'fee_total_usd': str, 'fee_per_kb': str, 'fee_per_kb_usd': str, 'fee_per_kwu': str,
                                                 'fee_per_kwu_usd': str, 'cdd_total': str, 'generation_usd': str, 'reward_usd': str,
                                                 'guessed_miner': str,
                                })
            Session = sessionmaker(bind=ENGINE)
            session = Session()
            for idx in range(len(df)):
                item = BlockStatistics(int(df.iloc[idx,0]),str(df.iloc[idx,1]),str(df.iloc[idx,2]),str(df.iloc[idx,3]),
                                       int(df.iloc[idx,4]),int(df.iloc[idx,5]),int(df.iloc[idx,6]),int(df.iloc[idx,7]),
                                       df.iloc[idx,8],df.iloc[idx,9],df.iloc[idx,10],int(df.iloc[idx,11]),
                                       int(df.iloc[idx,12]),Decimal(df.iloc[idx,13]),df.iloc[idx,14],df.iloc[idx,15],
                                       int(df.iloc[idx,16]),int(df.iloc[idx,17]),int(df.iloc[idx,18]),int(df.iloc[idx,19]),
                                       int(df.iloc[idx,20]),Decimal(df.iloc[idx,21]),int(df.iloc[idx,22]),
                                       Decimal(df.iloc[idx,23]),int(df.iloc[idx,24]),Decimal(df.iloc[idx,25]),
                                       Decimal(df.iloc[idx,26]),Decimal(df.iloc[idx,27]),Decimal(df.iloc[idx,28]),
                                       Decimal(df.iloc[idx,29]),Decimal(df.iloc[idx,30]),int(df.iloc[idx,31]),
                                       Decimal(df.iloc[idx,32]),int(df.iloc[idx,33]),Decimal(df.iloc[idx,34]),
                                       df.iloc[idx,35],
                                      )
    
                session.add(item)
            session.commit()
            session.close()


