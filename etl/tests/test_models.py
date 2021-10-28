'''Tests for ensuring that models match the API.
    Models are validated against the locally stored openapi JSON file, which the API we're using kindly provides.
    There is a separate test that checks whether the openapi schema of the API matches what we have, i.e. whether our
    information about the API is up-to-date.
'''

from etl.models import ReceiptCreate

def assert_schema_equality(a, b):
    '''Utility for checking important bits of schemas. Namely:
        -type and properties must be equal
        -required fields must be same, but order isn't significant
        -title is irrelevant
    '''
    type_a = a['type']
    type_b = b['type']

    assert type_a == type_b

    properties_a = a['properties']
    properties_b = b['properties']

    assert properties_a == properties_b

    # set probably best alternative: at least nothing can be "required twice", 
    # so we really only care about whether the sets are equal
    required_a = set(a['required'])
    required_b = set(b['required'])

    assert required_a == required_b


def test_receiptcreate(api_schema):
    model_schema = api_schema['components']['schemas']['ReceiptCreate']
    
    assert_schema_equality(model_schema, ReceiptCreate.schema())
