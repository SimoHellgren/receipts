from urllib import parse

import requests

from . import models


class ReceiptAPI(requests.Session):
    def __init__(self, baseurl, *args, **kwargs):
        self.baseurl = baseurl
        super().__init__(*args, **kwargs)

    def request(self, method, path, *args, **kwargs):
        url = parse.urljoin(self.baseurl, path)
        return super().request(method, url, *args, **kwargs)


    def get_receipts(self):
        return self.get('/receipts')


    def put_receipt(self, receipt: models.ReceiptCreate):
        return self.put('/receipts', data=receipt.json())
