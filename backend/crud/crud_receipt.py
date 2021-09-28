from .base import CRUDBase
from backend.models import Receipt as ReceiptModel
from backend.schemas import Receipt as ReceiptSchema, ReceiptCreate as ReceiptCreateSchema


receipt = CRUDBase[ReceiptModel, ReceiptCreateSchema, ReceiptSchema](ReceiptModel)
