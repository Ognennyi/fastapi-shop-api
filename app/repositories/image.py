from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.image import Image
from sqlalchemy import select, delete


class ImageRepository:

    async def create_image(self, session: AsyncSession, image: Image) -> Image:
        session.add(image)
        await session.flush()
        await session.refresh(image)
        return image
    
    async def get_by_id(self, session: AsyncSession, image_id: UUID) -> Image | None:
        find_image = select(Image).where(Image.id == image_id)
        result = await session.scalar(find_image)

        if result is None:
            return None
        return result
    
    async def image_delete(self, session: AsyncSession, image_id:UUID) -> bool:
        del_image = delete(Image).where(Image.id == image_id)
        result_response = await session.execute(del_image) 
        return result_response.rowcount > 0 
    
    async def image_update(self, session: AsyncSession, image_id:UUID, image_bytes:bytes ) -> Image | None:
        image = await session.get(Image, image_id)

        if image is None:
            return None
        
        image.image = image_bytes
        await session.flush()
        return image
    

    



# Для изображений:

#Done
# добавление изображения (на вход подается byte array изображения и id товара).

#Done
# Получение изображения конкретного товара (по id товара).   тоже самое что и   # Получение изображения по id изображения. 
# В Service надо будет получить продукт с id изображения и вызвать метод получения

#Done
# Удаление изображения по id изображения.
# 

#Done
# Изменение изображения (на вход подается id изображения и новая строка для замены).