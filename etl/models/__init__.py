'''Models to communicate with the API we're using.
   I could of course just use the ones I've defined in backend, as I'm the author of that, too, but
   this is more of an exercise, so I'm pretending as if I didn't write the backend and don't have access
   to the models. The idea is to ensure that we're always sending valid data by periodically comparing 
   the API's schema with the models we have. 
'''

from .receipt import ReceiptCreate
from .receiptline import Receiptline
