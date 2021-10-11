from .base import CRUDBase
from backend.app.models import Chain as ChainModel
from backend.app.schemas import Chain as ChainSchema

chain = CRUDBase[ChainModel, ChainSchema, ChainSchema](ChainModel)
