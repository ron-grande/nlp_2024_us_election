import os
import json
import time
import shutil
import sqlite3
import requests
from hashlib import sha256
from datetime import datetime, timedelta

# Collect config values from db
db_file_path = '../../../nlp_2024_us_election_db/nlp_dev'
db_conn = sqlite3.connect(db_file_path) # Establish connection to db
cursor = db_conn.cursor()
metadata_query_results = cursor.execute( #
    "SELECT * FROM config_vw_api_metadata WHERE 1=1  AND source_name = 'gnews' AND event_name = 'us 2022 midterm elections'"
    ).fetchall()[0] # Query for source and event details and collect

db_conn.close() # Close db connection

# Constants
GNEWS_API_KEY = os.environ['GNEWS_API_KEY']
DATA_SOURCE_NAME = metadata_query_results[0]
EVENT_NAME = metadata_query_results[1]
EVENT_START_DATE = metadata_query_results[2]
EVENT_END_DATE = metadata_query_results[3]
DATA_FORMAT = metadata_query_results[4]
DATA_SOURCE_TYPE = metadata_query_results[5]
API_URL = metadata_query_results[6]
DATA_DIR_PATH = '../../../DATA/gnews/midterms/stage/'

# Delete all content in staging folder for idempotency
for filename in os.listdir(DATA_DIR_PATH):
    file_path = os.path.join(DATA_DIR_PATH, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Convert event date range to datetime
date_range_min = datetime.strptime(EVENT_START_DATE, '%d %b %Y')
date_range_max = datetime.strptime(EVENT_END_DATE, '%d %b %Y')

# Prepare gnews request list
req_dicts = []
current_date = date_range_min

metadata_dict = {
        'source_name': DATA_SOURCE_NAME
        , 'event_name': EVENT_NAME
        , 'data_format': DATA_FORMAT
        , 'source_type': DATA_SOURCE_TYPE
    }

while current_date <= date_range_max:
    event_end_date_time = current_date.replace(hour=23, minute=59).strftime('%Y-%m-%dT%H:%M:%SZ')

    api_req_dict = metadata_dict.copy()
    api_req_dict['req_url'] = f"{API_URL}&from={current_date.strftime('%Y-%m-%dT%H:%M:%SZ')}&to={event_end_date_time}&apikey={GNEWS_API_KEY}"
    api_req_dict['event_start_date'] = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    api_req_dict['event_end_date'] = event_end_date_time

    req_dicts.append(api_req_dict)

    current_date += timedelta(days = 1)

file_dicts = []

# Request data from gnews
for i in range(len(req_dicts)):
    req_dict = req_dicts[i]

    print(f"{i + 1} GET {req_dict['req_url']}")
    r = requests.get(req_dict['req_url'])

    if not r.ok:
        print(req_dict)
        print(r.status_code)
        break

    time.sleep(3)

    json_payload = r.json()
    req_dict['article_count'] = len(json_payload['articles'])

    file_dicts.append({
        'gnews_api_data': json_payload
        , 'metadata': req_dict
    })

    url_api_key_param_xd = file_dicts[i]['metadata']['req_url'].replace(f'apikey={GNEWS_API_KEY}', 'apikey=xxx')
    file_dicts[i]['metadata']['req_url'] = url_api_key_param_xd
    record_id_str = file_dicts[i]['metadata']['source_name'] + file_dicts[i]['metadata']['event_name'] + file_dicts[i]['metadata']['event_start_date'] + file_dicts[i]['metadata']['event_end_date']
    record_id_hex = sha256(bytes(record_id_str, 'utf-8')).hexdigest()

    file_dicts[i]['metadata']['bronze_record_id'] = record_id_hex
    file_dicts[i]['metadata']['bln_isProcessedToSilver'] = 0
    
    for j in range(len(file_dicts[i]['gnews_api_data']['articles'])):
        article_id_str = record_id_hex + file_dicts[i]['gnews_api_data']['articles'][j]['title'] + file_dicts[i]['gnews_api_data']['articles'][j]['source']['name'] + file_dicts[i]['gnews_api_data']['articles'][j]['publishedAt']
        article_id_hex = sha256(bytes(article_id_str, 'utf-8')).hexdigest()

        file_dicts[i]['gnews_api_data']['articles'][j]['bronze_article_id'] = article_id_hex

for record in file_dicts:
    dtm = datetime.now()
    dtm_str = dtm.strftime('%Y%m%d%H%M%S') + f"{dtm.microsecond // 1000:03d}"

    file_name = f"{dtm_str}.{DATA_FORMAT}"

    with open(f'{DATA_DIR_PATH}{file_name}', 'w') as f:
        f.write(json.dumps(record))
