'''Tests for ensuring that models match the API.
    Models are validated against the locally stored openapi JSON file, which the API we're using kindly provides.
    There is a separate test that checks whether the openapi schema of the API matches what we have, i.e. whether our
    information about the API is up-to-date.
'''

from etl import models

from .utils import openapi_component_schema_match

def test_receiptcreate(api_schema):
    model_schema = api_schema['components']['schemas']['ReceiptCreate']
    
    assert openapi_component_schema_match(model_schema, models.ReceiptCreate.schema())


def test_receiptline(api_schema):
    model_schema = api_schema['components']['schemas']['Receiptline']

    assert openapi_component_schema_match(model_schema, models.Receiptline.schema())
