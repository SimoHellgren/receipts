from .base import CRUDBase
from backend.models import Product as ProductModel
from backend.schemas import Product as ProductSchema, ProductCreate as ProductCreateSchema

product = CRUDBase[ProductModel, ProductCreateSchema, ProductSchema](ProductModel)