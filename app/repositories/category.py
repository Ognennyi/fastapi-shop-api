from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from sqlalchemy import select


class CategoryRepository:

    async def create_category(self, session: AsyncSession, category: Category) -> Category:
        session.add(category)
        await session.flush()
        await session.refresh(category)
        return category
    
    async def get_by_id(self, session: AsyncSession, category_id: UUID) -> Category | None:
        find_category = select(Category).where(Category.id == category_id)
        result = await session.scalar(find_category)

        if result is None:
            return None
        return result
    
    
    async def get_all(self, session: AsyncSession) -> list[Category]:
        categories = select(Category)
        request = await session.scalars(categories)
        request = request.all()
        return request

    



