import io
import json
from datetime import datetime, timezone, timedelta
from os import listdir, environ
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Define the scopes needed for the script
SCOPES = ['https://www.googleapis.com/auth/drive']

# gdrive credentials file
SERVICE_ACCOUNT_FILE = '../../../token.json'
# Bronze layer dir 
GNEWS_BRONZE_FOLDER_ID = environ['GNEWS_BRONZE_FOLDER_ID']

MIDTERMS_FILES_PATH = '../../../DATA/gnews/midterms/bronze/'

# Authenticate using the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build Google Drive service
service = build('drive', 'v3', credentials=credentials)

file_paths = [MIDTERMS_FILES_PATH + i for i in listdir(MIDTERMS_FILES_PATH)]
# batch_size = 10
# file_batches = [file_paths[i:i + batch_size] for i in range(0, len(file_paths))]

for file_path in file_paths:
    with open(file_path, 'r') as f:
        file_dict = json.loads(f.read())
        file_dict['metadata']['dtm_DatetimeUploaded'] = datetime.now(timezone(timedelta(hours=10))).strftime("%Y-%m-%dT%H:%M:%S%z") 

        # Create an in-memory stream
        fh = io.BytesIO(bytes(json.dumps(file_dict['gnews_api_data']), 'utf-8'))

        dtm = datetime.now()
        dtm_str = dtm.strftime('%Y%m%d%H%M%S')

        file_name = f"{dtm_str}.json"

        file_metadata = {
            'name' :file_name
            , 'parents': [GNEWS_BRONZE_FOLDER_ID]
            # , 'properties': file_dict['metadata']
        }

        media = MediaIoBaseUpload(fh, mimetype='application/json')

        file = service.files().create(
            body=file_metadata
            , media_body=media
            , fields='id'
        ).execute()

        print(f'File ID: {file.get("id")}')

