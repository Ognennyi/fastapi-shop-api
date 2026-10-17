
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse








def to_product_model(data: ProductCreate) -> Product:
    return Product(
        name = data.name,
        category_id= data.category_id,
        price = data.price,
        available_stock = data.available_stock,
        supplier_id = data.supplier_id
    )
    


def to_product_response(data: Product) -> ProductResponse:
    return ProductResponse(
        id = data.id,
        name = data.name,
        category_id=data.category_id,
        price = data.price,
        available_stock= data.available_stock,
        last_update_date= data.last_update_date,
        supplier_id= data.supplier_id,
        image_id= data.image_id
    )
    
