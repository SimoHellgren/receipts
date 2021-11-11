'''A utility script to download and store the current schema of API_URL.
    While we could just dump the response directly into a file (since it is JSON already),
    we convert it so json.dump can add nice indentantion for readability.
'''

import os
import json

import requests

from dotenv import load_dotenv

def main():
    load_dotenv()

    API_URL = os.getenv('API_URL')

    schema = requests.get(API_URL + '/openapi.json')

    with open('etl/receipt_api_schema.json', 'w') as f:
        json.dump(schema.json(), f, indent=2) 


if __name__ == '__main__':
    main()