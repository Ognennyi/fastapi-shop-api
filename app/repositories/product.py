from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from sqlalchemy import select, delete

class ProductRepository:

    async def create_product(self, session: AsyncSession, product: Product) -> Product:
        session.add(product)
        await session.flush()
        await session.refresh(product)
        return product 
    
    
    async def get_by_id(self, session: AsyncSession, product_id: UUID) -> Product | None:
        find_product = select(Product).where(Product.id == product_id)
        result = await session.scalar(find_product)

        if result is None:
            return None
        return result
    
    
    async def get_all(self, session: AsyncSession) -> list[Product]:
        products = select(Product).where(Product.available_stock > 0)
        request = await session.scalars(products)
        request = request.all()
        return request
    
    async def product_delete(self, session: AsyncSession, product_id:UUID) -> bool:
        del_product = delete(Product).where(Product.id == product_id)
        result_response = await session.execute(del_product) 
        return result_response.rowcount > 0 
    

    async def product_downgrade(self, session: AsyncSession, product_id:UUID, count:int) -> Product | None:   # count - какое число встанет на место предыдущего
        product = await session.get(Product, product_id)

        if product is None:
            return None
        
        product.available_stock = count
        await session.flush()
        return product
    


    async def product_update_image(self, session: AsyncSession, product_id:UUID, image_id: UUID) -> Product | None:
        product = await session.get(Product, product_id)

        if product is None:
            return None
        
        product.image_id = image_id
        await session.flush()
        return product
    

# Для товаров:

#Done
# Добавление товара (на вход подается json, соответствующей структуре, описанной сверху).

#Done
# Получение товара по id.

#Done
# Получение всех доступных товаров.

#Done
# Уменьшение количества товара (на вход запросу подается id товара и на сколько уменьшить).

#Done
# Удаление товара по id.