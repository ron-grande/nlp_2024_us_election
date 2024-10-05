import os
import json
import time
import sqlite3
import requests
from hashlib import sha256
from datetime import datetime, timedelta

# Collect config values from db
db_file_path = '../../nlp_2024_us_election_db/nlp_dev'
db_conn = sqlite3.connect(db_file_path)
cursor = db_conn.cursor()
metadata_query_results = cursor.execute("SELECT * FROM config_vw_api_metadata WHERE source_name = 'gnews'").fetchall()[0]
metadata_query_results
db_conn.close()

# Constants
GNEWS_API_KEY = os.environ['GNEWS_API_KEY']
DATA_SOURCE_NAME = metadata_query_results[0]
EVENT_NAME = metadata_query_results[1]
EVENT_START_DATE = metadata_query_results[2]
EVENT_END_DATE = metadata_query_results[3]
DATA_FORMAT = metadata_query_results[4]
DATA_SOURCE_TYPE = metadata_query_results[5]
API_URL = metadata_query_results[6]
DATA_DIR_PATH = '../../DATA/gnews/midterms/'

# Convert event date range to datetime
date_range_min = datetime.strptime(EVENT_START_DATE, '%d %b %Y')
date_range_max = datetime.strptime(EVENT_END_DATE, '%d %b %Y')

# Prepare gnews request list
req_dicts = []
current_date = date_range_min

metadata_dict = {
        'source_name': DATA_SOURCE_NAME
        , 'event': EVENT_NAME
        , 'data_format': DATA_FORMAT
        , 'source_type': DATA_SOURCE_TYPE
    }

while current_date <= date_range_max:
    event_end_date_time = current_date.replace(hour=23, minute=59).strftime('%Y-%m-%dT%H:%M:%SZ')

    api_req_dict = metadata_dict
    api_req_dict['req_url'] = f"{API_URL}&from={current_date.strftime('%Y-%m-%dT%H:%M:%SZ')}&to={event_end_date_time}&apikey={GNEWS_API_KEY}"
    api_req_dict['event_start_date'] = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    api_req_dict['event_end_date'] = event_end_date_time

    req_dicts.append(api_req_dict)

    current_date += timedelta(days = 1)

# Request data from gnews
for i in range(len(req_dicts)):
    req_dict = req_dicts[i]

    r = requests.get(req_dict['req_url'])

    if not r.ok:
        print(req_dict)
        print(r.status_code)
        break

    time.sleep(3)

    json_payload = r.json()
    req_dict['article_count'] = len(json_payload['articles'])

    req_dicts[i] = {
        'gnews_api_data': json_payload
        , 'metadata': req_dict
    }

    url_api_key_param_xd = req_dicts[i]['metadata']['req_url'].replace(f'apikey={GNEWS_API_KEY}', 'apikey=xxx')
    req_dicts[i]['metadata']['req_url'] = url_api_key_param_xd
    record_id_str = req_dicts[i]['metadata']['source_name'] + req_dicts[i]['metadata']['event'] + req_dicts[i]['metadata']['event_start_date'] + req_dicts[i]['metadata']['event_end_date']
    record_id_hex = sha256(bytes(record_id_str, 'utf-8')).hexdigest()

    req_dicts[i]['metadata']['bronze_record_id'] = record_id_hex
    req_dicts[i]['metadata']['bln_isProcessedToSilver'] = 0
    
    for j in range(len(req_dicts[i]['gnews_api_data']['articles'])):
        article_id_str = record_id_hex + req_dicts[i]['gnews_api_data']['articles'][j]['title'] + req_dicts[i]['gnews_api_data']['articles'][j]['source']['name'] + req_dicts[i]['gnews_api_data']['articles'][j]['publishedAt']
        article_id_hex = sha256(bytes(article_id_str, 'utf-8')).hexdigest()

        req_dicts[i]['gnews_api_data']['articles'][j]['bronze_article_id'] = article_id_hex
    

for record in req_dicts:
    dtm = datetime.now()
    dtm_str = dtm.strftime('%Y%m%d%H%M%S')

    file_name = f"{dtm_str}.{DATA_FORMAT}"

    with open(f'{DATA_DIR_PATH}{file_name}', 'w') as f:
        f.write(json.dumps(record))
