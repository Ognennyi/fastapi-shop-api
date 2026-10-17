


from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import Image

from app.schemas.product import ProductResponse

from app.repositories.image import ImageRepository
from app.repositories.product import ProductRepository

from app.mappers.image_mappers import to_image_model

from app.mappers.product_mappers import to_product_response

from app.core.exceptions import NotFoundError, ConflictError







class ImageService:
    def __init__(self, rep_image: ImageRepository, rep_product: ProductRepository):
        self.rep_image = rep_image
        self.rep_product = rep_product

    
    async def create_image(self, session: AsyncSession, product_id: UUID, images_bytes: bytes) -> ProductResponse:
        
        find_product = await self.rep_product.get_by_id(session, product_id)
        if find_product is None:
            raise NotFoundError("Product not found")
        
        if find_product.image_id is not None:
            raise ConflictError("Product already has an image")

        image_model = to_image_model(images_bytes)

        created_image = await self.rep_image.create_image(session, image_model)
        
        update_image_in_product = await self.rep_product.product_update_image(session, product_id, created_image.id)

        if update_image_in_product is None:
            raise NotFoundError("Product not found")
        
        response = to_product_response(update_image_in_product)

        await session.commit()
        
        return response
    

    async def get_image_by_id(self, session: AsyncSession, image_id: UUID) -> Image:

        find_image = await self.rep_image.get_by_id(session, image_id)
        if find_image is None:
            raise NotFoundError("Image not found")
        
        return find_image
    
    async def get_image_by_product_id(self, session: AsyncSession, product_id: UUID) -> Image:

        find_product = await self.rep_product.get_by_id(session, product_id)
        if find_product is None:
            raise NotFoundError("Product not found")
        
        if find_product.image_id is None:
            raise NotFoundError("Image not found")

        find_image = await self.rep_image.get_by_id(session, find_product.image_id)
        if find_image is None:
            raise NotFoundError("Image not found")
        
        return find_image

    async def delete_image(self, session: AsyncSession, image_id: UUID) -> bool:
        image = await self.rep_image.get_by_id(session, image_id)
        if image is None:
            raise NotFoundError("Image not found")
        
        deleted_image = await self.rep_image.image_delete(session, image_id)
        await session.commit()
        return deleted_image
    

    async def update_image(self, session: AsyncSession, image_id: UUID, new_image_bytes: bytes) -> Image:
        
        find_image = await self.rep_image.get_by_id(session, image_id)
        if find_image is None:
            raise NotFoundError("Image not found")
        
        updated_image = await self.rep_image.image_update(session, image_id, new_image_bytes)
        if updated_image is None:
            raise NotFoundError("Image not found")
         
        await session.commit()

        return updated_image


        


        



# Для изображений:

# добавление изображения 
# (на вход подается byte array изображения и id товара). DONE

# Изменение изображения 
# (на вход подается id изображения и новая строка для замены). DONE 

# Удаление изображения по id изображения. DONE 

# Получение изображения конкретного товара (по id товара).DONE

# Получение изображения по id изображения.DONE