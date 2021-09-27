from .base import CRUDBase
from backend.models import Store as StoreModel
from backend.schemas import Store as StoreSchema, StoreCreate as StoreCreateSchema

store = CRUDBase[StoreModel, StoreCreateSchema, StoreSchema](StoreModel)
