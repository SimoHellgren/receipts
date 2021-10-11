from typing import Any, List

from sqlalchemy.orm import Session

from .base import CRUDBase
from backend.app.models import Receiptline as ReceiptlineModel
from backend.app.schemas import Receiptline as ReceiptlineSchema, ReceiptlineCreate as ReceiptlineCreateSchema

class CRUDReceiptline(CRUDBase[ReceiptlineModel, ReceiptlineCreateSchema, ReceiptlineSchema]):
    def get_by_receipt(self, db: Session, receipt_id: Any) -> List[ReceiptlineModel]:
        return (
            db.query(self.model)
            .filter(self.model.receipt_id == receipt_id)
            .all()
        )


receiptline = CRUDReceiptline(ReceiptlineModel)
