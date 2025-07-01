import os
import requests
import pandas as pd
from dotenv import load_dotenv

#SOURCE_PATH = 'data/fake_model.csv'
SOURCE_PATH = 'data/models.csv'
DEST_PATH = 'data/seriesCode_BYD.csv'

def get_seriesCode(vin: str):
    load_dotenv()
    URL = str(os.getenv('URL'))
    headers = {
        "Content-Type": "application/json",
        "APP_ID": os.getenv('GB_APP_ID'),
        "SECRET_KEY": os.getenv('GB_SECRET_KEY'),
        "encrypt": os.getenv('ENCRYPT'),
        "request_from": os.getenv('REQUEST_FROM'),
        "lang-type": os.getenv('LANG_TYPE'),
    }

    payload = {
        "vin": f"{vin}"
    }

    response = requests.post(url=URL, json=payload, headers=headers)
    data = response.json()
    if len(data['data']) > 0:
        code = data['data']['seriesCode']
    else:
        code = ''
    return code


series_code = []
df = pd.read_csv(SOURCE_PATH, sep=';')

for x, row in df.iterrows():
    code = get_seriesCode(row['CHASSI_COMPLETO'])
    series_code.append(code)

df['SERIES_CODE'] = series_code

pd.DataFrame.to_csv(df, DEST_PATH, index=False)
print(df)