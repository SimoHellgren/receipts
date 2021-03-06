'''utilities for extracting various bits from raw receipt text'''

import re
from itertools import takewhile
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class ReceiptItemLine:
    '''An item line on a receipt'''
    line_num: int
    product: str
    price: int


@dataclass
class Receipt:
    id: str
    total: int
    reprint: str
    datetime: str
    paymentmethod: str = field(init=False)
    items: Iterable[ReceiptItemLine] = field(init=False)

    def __post_init__(self):
        self.paymentmethod = extract_payment_method(self.reprint)
        self.items = extract_items(self.reprint)


@dataclass
class Chain:
    id: str
    name: str


@dataclass
class Store:
    id: str
    name: str


@dataclass
class ParsingResult:
    '''A contract / interface between the Transform and Load steps'''
    receipt: Receipt 
    chain: Chain
    store: Store
    etag: str


def extract_payment_method(reprint: str, default: str = 'CASH') -> str:
    ''' searches for patterns like **** **** **** 1234
        and returns the first one, or a default value
    '''
    pattern = r'\*{4} \*{4} \*{4} \d{4}'
    cards = re.findall(pattern, reprint, re.I)

    return next(iter(cards), default)


def parse_price(price: str) -> int:
    if price.endswith('-'): # move negative sign to front
        price = f'-{price[:-1]}'
    
    # return an integer amount of cents
    return int(float(price.replace(',', '.')) * 100)


def extract_items(reprint: str) -> Iterable[ReceiptItemLine]:
    '''Look for anything that ends in a price.
        Ignore total-looking rows
        Ignore rows starting with whitespace (K-group's discounts)
        -these could be handled more elegantly, later
        Stopwords terminate the process
        -anything related to payments
    '''
    price_pattern = (
        r'('                 # group for re.split functionality
        r'\d{1,3}[\.,]\d{2}' # price of 3.2 digits
        r'\s?[€|EUR]?\s?'    # with perhaps a eurosign
        r'\-?'               # might be negative
        r'$'                 # row end
        r')'                 # close group
    )

    ignore = r'yhteensä|total'
    stopwords = r'korttitapahtuma|käteinen|maksettu plussa-rahalla|kortti:'

    stop = takewhile(lambda x: not re.search(stopwords, x[1], re.I), enumerate(reprint.split('\n')))
    has_price = filter(lambda x: re.search(price_pattern, x[1], re.I), stop)
    not_total = filter(lambda x: not re.search(ignore, x[1], re.I), has_price)
    no_ws_start = filter(lambda x: not x[1].startswith(' '), not_total)

    # split to get names and prices
    for i, item in no_ws_start:
        name, price, *_ = (e.strip() for e in re.split(price_pattern, item, re.I))

        yield ReceiptItemLine(i, name, parse_price(price))
