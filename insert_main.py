import requests
import pandas as pd
from core.keys import PRIVATE_TOKEN
from core.configs import settings
import json
from sqlalchemy.sql import text
import sqlalchemy

tipos_status = ['NP','ER','PHT' ]
novos_registros = []
api_key = PRIVATE_TOKEN
headers = {'X-Auth-Token': api_key}

for status in tipos_status:
    url = f'https://ws-bomi-biotracker.bionexo.com/Rest/MovimentoEstoque.svc/Check?status={status}'
    req = requests.get(url, headers=headers)
    convert_json = req.json()
    decoder_jayson = json.loads(convert_json) 
    
    for item in decoder_jayson:
        novos_registros.append([item['ID_INTEGRATION'],
                                item['DS_FROM_DISPOSITION'],
                                item['DS_USER'],
                                item['DS_TRANSACTION_PICKING'],
                                item['DS_ITEM_REF'],
                                item['DS_ITEM_LOT'],
                                item['DS_FROM_LOCATION'],
                                item['DT_WRITE']])
            
        df = pd.DataFrame(novos_registros, columns=['T7IDIN',
                                                    'T7WHS',
                                                    'T7REFB',
                                                    'T7REFA',
                                                    'T7SKU',
                                                    'T7LOTN',
                                                    'T7LCFR',
                                                    'T7DTTR'] )
        
        db_connection = settings.DB_URL
        engine = sqlalchemy.create_engine(db_connection)
        sql = '''SELECT * FROM "WTABB" '''
        with engine.connect().execution_options(auto_commit=True) as conn:
            query = conn.execute(text(sql)).fetchall()
            for inf in novos_registros[0]:
                if inf not in query[0]:
                    df.to_sql(con=db_connection, name="WTABB", if_exists='append', index=False)
                    print("Dados gravados com sucesso")

