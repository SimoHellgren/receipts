'''Test that the API calls that we're making our valid.

   Mostly, we're doing contract testing here, where we check against our locally saved OpenAPI schema that:
   -the endpoints we're calling exist
   -the endpoint accepts the HTTP verb of our call
   -we're sending data that the endpoint expects
    -this is done a bit weirdly, though:
        1. check that the method we're using has a type annotation for a model that matches the schema
        2. check that the data we send can be parsed with said model
    -but, there isn't really a clear way to abstract / generalize this yet (maybe not that necessary, at least now)
    -there's also some duplication: test_models.py already validates models against the schema
    -might be that generalizing this or automating second-order testing is super-overengineering
    -it also feels weird that there's no runtime checking of the data, and pydantic is just used for type annotation
     -though perhaps static type checking might be enough here?

'''

import json

from etl.receipt_api import ReceiptAPI

from .utils import openapi_component_schema_match, check_path_match, traverse_nested_dict, find


def test_put_receipt(mocker, test_data, api_schema):
    '''a test for the existence of the path that we're sending api requeqests at
        check for:
         -path exists
         -path supports verb
         -data sent parses to something the API expects
    '''

    api_paths = api_schema['paths']
    test_receipt = test_data['receipt']
    mocker.patch.object(ReceiptAPI, 'request', return_value='test')

    api = ReceiptAPI('http://localhost/')


    # can we replace this with static type checking?
    result=api.put_receipt(test_receipt)

    call_method, call_path = api.request.call_args.args
    data = api.request.call_args.kwargs['data']

    # check that there is matching path
    matching_path = find(lambda p: check_path_match(call_path, p), api_paths)

    assert matching_path

    verb_spec = api_paths[matching_path].get(call_method.lower())
    
    # check that HTTP verb is valid
    assert verb_spec

    # check parameters, data etc
    
    # how do we do this in the general case?
    # and what about things that are not in the request body?
    body_schema_ref = verb_spec['requestBody']['content']['application/json']['schema']['$ref'].split('/')[1:]
    body_schema = traverse_nested_dict(body_schema_ref, api_schema)

    # how would this generalize?
    model = api.put_receipt.__annotations__.get('receipt')

    assert openapi_component_schema_match(body_schema, model.schema())

    # check that data parses
    assert model(**json.loads(data))
