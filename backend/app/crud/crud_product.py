from .base import CRUDBase
from backend.app.models import Product as ProductModel
from backend.app.schemas import Product as ProductSchema, ProductCreate as ProductCreateSchema

product = CRUDBase[ProductModel, ProductCreateSchema, ProductSchema](ProductModel)