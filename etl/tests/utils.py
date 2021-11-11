'''Utility functions for testing things about OpenAPI schemas
'''

import re

find = lambda function, iterable, default=None: next(filter(function, iterable), default)

def openapi_component_schema_match(a, b):
    '''Check whether two OpenAPI components match, at least where relevant: 
        -types must be equal
        -properties must be equal
        -required fields must be same, but order isn't significant
        -title is irrelevant, as we can name models as we please

       TODO: unit tests for this function
       TODO: also I'm not sure I like the many returns here, but oh well 
    '''

    type_a = a['type']
    type_b = b['type']

    if type_a != type_b:
        return False

    properties_a = a['properties']
    properties_b = b['properties']

    if properties_a != properties_b:
        return False

    # set probably best alternative: at least nothing can be "required twice", 
    # so we really only care about whether the sets are equal
    required_a = set(a['required'])
    required_b = set(b['required'])

    return required_a == required_b


def check_path_match(call_path: str, schema_path: str) -> bool:
    '''Given a path that was used in an API call and a path from an OpenAPI schema,
        check whether the API call path matches the OpenAPI schema path
        Example (spacing is funky on purpose):
         check_path_match( '/receipts/'    , '/receipts'              ) --> True
         check_path_match( '/receipts/123' , '/receipts/{receipt_id}' ) --> True
         check_path_match( '/receipt/123'  , '/receipts/{receipt_id}' ) --> False
         check_path_match( '/receipts'     , '/receipts/{receipt_id}' ) --> False

       TODO: unit tests for this function itself
    '''
    # separate by /
    call_parts = [e for e in call_path.split('/') if e]
    schema_parts = [e for e in schema_path.split('/') if e]

    # path doesn't match if there is a different number of "parts"
    if len(call_parts) != len(schema_parts):
        return False


    # regex for matching parameters, like {param} or {param:int}
    # params must start with a letter, but can contain numbers and underscores, too 
    PARAM_REGEX = re.compile("^{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}$")

    for call_part, schema_part in zip(call_parts, schema_parts):
        
        # if schema_part looks like a parameter, basically anything goes (for now)
        if PARAM_REGEX.match(schema_part):
            # TODO: if we know the type of the parameter, we can check that what was provided is valid
            continue

        # otherwise, call_part and schema_part must be exact matches
        elif call_part != schema_part:
            return False

    return True


def traverse_nested_dict(keys: list, d: dict):
    '''Example:
        traverse_nested_dict(['a', 'b'], {'a': {'b': {'c': 1}}}) --> {'c': 1}

        TODO: unit tests maybe?
    '''
    if not keys:
        return d
    
    key, *rest = keys
    d_ = d[key]

    return traverse_nested_dict(rest, d_)
