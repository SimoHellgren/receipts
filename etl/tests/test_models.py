'''Tests for ensuring that models match the API.
    Models are validated against the locally stored openapi JSON file, which the API we're using kindly provides.
    There is a separate test that checks whether the openapi schema of the API matches what we have, i.e. whether our
    information about the API is up-to-date.
'''

from etl import models

from .utils import openapi_component_schema_match


def compare_schema_component_with_model(schema, component_name, model):
    '''Utility for reuse'''
    model_schema = schema['components']['schemas'][component_name]

    return openapi_component_schema_match(model_schema, model.schema())


def test_receiptcreate(api_schema):
    assert compare_schema_component_with_model(api_schema, 'ReceiptCreate', models.ReceiptCreate)


def test_receiptline(api_schema):
    assert compare_schema_component_with_model(api_schema, 'Receiptline', models.Receiptline)

