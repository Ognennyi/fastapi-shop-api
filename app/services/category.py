

from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.category import CategoryCreate, CategoryResponse
from app.repositories.category import CategoryRepository

from app.mappers.category_mappers import to_category_model, to_category_response

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictError


class CategoryService:

    def __init__(self, rep_category: CategoryRepository):
        self.rep_category = rep_category

    
    async def create_category(self, session: AsyncSession, category: CategoryCreate ) -> CategoryResponse:
        try:
            category_model = to_category_model(category)
            create_category = await self.rep_category.create_category(session, category_model)

            response = to_category_response(create_category)
            
            await session.commit()
            return response
        
        except IntegrityError:
            await session.rollback()
            raise ConflictError("Category with this name already exists") 
    
    async def get_all(self, session: AsyncSession) -> list[CategoryResponse]:

        categories_list = await self.rep_category.get_all(session)

        categories_response = []
        for category in categories_list:
            categories_response.append(to_category_response(category))

        return categories_response



