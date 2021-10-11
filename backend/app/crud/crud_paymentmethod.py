from .base import CRUDBase
from backend.app.models import Paymentmethod as PaymentmethodModel
from backend.app.schemas import Paymentmethod as PaymentmethodSchema

paymentmethod = CRUDBase[PaymentmethodModel, PaymentmethodSchema, PaymentmethodSchema](PaymentmethodModel)