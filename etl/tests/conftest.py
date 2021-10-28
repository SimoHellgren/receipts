
import json

import pytest

@pytest.fixture(scope='session')
def api_schema():
    with open('etl/receipt_api_schema.json', 'rb') as f:
        return json.load(f)
