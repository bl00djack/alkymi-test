"""
APScheduler jobs
"""
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import traceback

from app.config import Config
from app.models.data_files import DataFile, Temporal
from app.serializers import TemporalSerializer


class StanfordNLPAPI:
    def __init__(self):
        token_url = 'https://alkymi-staging.auth0.com/oauth/token'
        audience = 'stanford-public.alkymi.cloud'
        client = BackendApplicationClient(client_id=Config.STANFORDAPI.client_id)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(
            token_url=token_url,
            client_id=Config.STANFORDAPI.client_id,
            client_secret=Config.STANFORDAPI.client_secret,
            audience=audience
        )

    def get_temporal(self, text):
        # Make an authenticated API request
        api_url = 'https://stanford-public.alkymi.cloud/getTemporals'
        headers = {'Authorization': 'Bearer ' + self.token['access_token']}
        response = requests.get(api_url, headers=headers, params={'text': text})
        return response.json()


def process_data_file():
    data_file = DataFile.objects.filter(file_status='processing', lock=False).first()
    if data_file:
        # Lock the file to prevent race condition between APScheduler workers
        data_file.lock = True
        data_file.save()
        # Initialize the API
        stanford_api = stanford_api = StanfordNLPAPI()
    else:
        return

    try:
        print(f"Processing file_id: {data_file._id}")
        temporal_columns = []  # indices of temporal columns
        temporals = []

        if data_file.has_header_row:
            for temporal_idx, header in enumerate(data_file.header):
                if 'date' in header.lower() or 'time' in header.lower():
                    temporal_columns.append(temporal_idx)
        else:
            first_row = data_file.rows[0]
            for temporal_idx, cell in enumerate(first_row):
                r = stanford_api.get_temporal(cell)
                if r:
                    temporal_columns.append(temporal_idx)

        print(f"Found {len(temporal_columns)} temporal columns.")
        if temporal_columns:
            for row_number, row in enumerate(data_file.rows):
                for idx in temporal_columns:
                    r = stanford_api.get_temporal(row[idx])
                    r[0].update({'row': row_number, 'column': idx})
                    temporal = TemporalSerializer().load(r[0])
                    temporals.append(Temporal(**temporal))
    except Exception as exc:
        data_file.lock = False
        data_file.save()
        print(f"Got interrupted while processing file_id: {data_file._id}")
        print(traceback.format_exc())
        return

    data_file.temporals = temporals
    data_file.file_status = 'finished'
    data_file.save()
    print(f"Finished processing file_id: {data_file._id}")
