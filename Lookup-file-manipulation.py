import pandas as pd 
import json
import logging
from pathlib import Path

#read config file
with open('LookupConfig.json') as json_file:
    data_config = json.load(json_file)

logging.basicConfig(level = logging.INFO)

def generate_json(dataframe):
    series_data = dataframe.groupby("Agence").apply(lambda row: row.to_json(orient='records'))
    return series_data.items()

def save_json(list_dic_json, base_path):
    for json_file_name, json_data in list_dic_json:
        base_path = Path(base_path)
        base_path.mkdir(parents=True, exist_ok=True)
        full_path = Path(base_path, json_file_name).with_suffix('.json')
        with open(full_path, 'w', encoding='UTF-8') as outfile:
             json.dump(json.loads(json_data), outfile, indent=2)
        logging.info('Json generated: %s', full_path)


df_lookups = pd.read_excel(data_config['ExcelInputPath'])
#df.drop('column_name', axis=1, inplace=True)
df_lookups_en = df_lookups.drop("Nom", axis=1)
df_lookups_fr = df_lookups.drop("Prenom", axis =1)

json_lookups_en = generate_json(df_lookups_en)
json_lookups_fr = generate_json(df_lookups_fr)

save_json(json_lookups_en, data_config['ExcelInputPath'] + '/en')
save_json(json_lookups_fr, data_config['ExcelInputPath'] + '/fr')


