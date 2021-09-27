from .base import CRUDBase
from backend.models import Paymentmethod as PaymentmethodModel
from backend.schemas import Paymentmethod as PaymentmethodSchema

paymentmethod = CRUDBase[PaymentmethodModel, PaymentmethodSchema, PaymentmethodSchema](PaymentmethodModel)