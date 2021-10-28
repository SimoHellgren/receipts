'''Test that receipt_api_schema is up-to-date, i.e. that the API is what our tests expect it to be'''

import os

import requests
from dotenv import load_dotenv


load_dotenv()

APIURL = os.getenv('API_URL')

def test_api_schema(api_schema):

    live_schema = requests.get(APIURL + '/openapi.json').json()

    assert live_schema == api_schema
