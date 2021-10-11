from .base import CRUDBase
from backend.app.models import Receipt as ReceiptModel
from backend.app.schemas import Receipt as ReceiptSchema, ReceiptCreate as ReceiptCreateSchema


receipt = CRUDBase[ReceiptModel, ReceiptCreateSchema, ReceiptSchema](ReceiptModel)
