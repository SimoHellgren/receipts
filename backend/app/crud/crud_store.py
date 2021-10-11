from .base import CRUDBase
from backend.app.models import Store as StoreModel
from backend.app.schemas import Store as StoreSchema, StoreCreate as StoreCreateSchema

store = CRUDBase[StoreModel, StoreCreateSchema, StoreSchema](StoreModel)
