from .base import CRUDBase
from backend.models import Chain as ChainModel
from backend.schemas import Chain as ChainSchema

chain = CRUDBase[ChainModel, ChainSchema, ChainSchema](ChainModel)
