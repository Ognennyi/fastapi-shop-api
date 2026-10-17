

from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.product import ProductCreate, ProductResponse

from app.repositories.image import ImageRepository
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.repositories.supplier import SupplierRepository

from app.mappers.product_mappers import to_product_model, to_product_response

from app.core.exceptions import NotFoundError, BadRequestError


class ProductService:

    def __init__(self, rep_product: ProductRepository, rep_image: ImageRepository, rep_category: CategoryRepository, rep_supplier: SupplierRepository):
        self.rep_product = rep_product
        self.rep_image = rep_image
        self.rep_category = rep_category
        self.rep_supplier = rep_supplier

    
    async def create_product(self, session: AsyncSession, data: ProductCreate) -> ProductResponse:

        find_category = await self.rep_category.get_by_id(session, data.category_id)
        if find_category is None:
            raise NotFoundError("Category not found")
        
        find_supplier = await self.rep_supplier.get_by_id(session, data.supplier_id)
        if find_supplier is None:
            raise NotFoundError("Supplier not found")
        
        product_model = to_product_model(data)
        product_model.category_id = find_category.id

        create_product = await self.rep_product.create_product(session, product_model)
        product_response = to_product_response(create_product)

        await session.commit()

        return product_response
    


    async def get_by_id(self, session: AsyncSession, product_id: UUID) -> ProductResponse:

        find_product = await self.rep_product.get_by_id(session, product_id)
        if find_product is None:
            raise NotFoundError("Product not found")


        product_response = to_product_response(find_product)
        return product_response

    

    async def get_all_products(self, session: AsyncSession) -> list[ProductResponse]:
        products = await self.rep_product.get_all(session)
        products_response = [] 
        for product in products:
            products_response.append(to_product_response(product))

        return products_response
    


    async def delete_product(self, session: AsyncSession, product_id: UUID) -> bool:
        product = await self.rep_product.get_by_id(session, product_id)
        if product is None:
            raise NotFoundError("Product not found")
        
        image_id = product.image_id
        
        deleted_product = await self.rep_product.product_delete(session, product_id)
        if image_id is not None:
            await self.rep_image.image_delete(session, image_id)

        await session.commit()
        return deleted_product
    

    async def deacrease_stock(self, session: AsyncSession, product_id: UUID, decrease: int) -> ProductResponse:

        product = await self.rep_product.get_by_id(session, product_id)

        if product is None :
            raise NotFoundError("Product not found") 
        
        if product.available_stock - decrease < 0:
            raise BadRequestError("count < 0")
        
        count = product.available_stock - decrease

        result = await self.rep_product.product_downgrade(session, product_id, count)
        
        await session.commit()

        return to_product_response(result)
