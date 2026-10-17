from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category import CategoryService

from app.dependencies import get_category_service

from app.schemas.common import ErrorResponse


router = APIRouter(tags = ["Categories"])



@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=201,
    summary="Добавить категорию",
    description="Создаёт новую категорию товаров.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации данных категории",
        },
        409: {
            "model": ErrorResponse,
            "description": "Категория с таким именем уже существует",
        },
    },
)
async def create_category(
                        data: CategoryCreate ,
                        session: AsyncSession = Depends(get_session), 
                        category_service: CategoryService = Depends(get_category_service)):
    
    created_category = await category_service.create_category(session, data)

    return created_category





@router.get(
    "/categories",
    response_model=list[CategoryResponse],
    status_code=200,
    summary="Получить категории",
    description=(
        "Возвращает список всех категорий товаров. "
        "Если категорий нет, возвращается пустой список."
    ),
)
async def get_all_categories(
                        session: AsyncSession = Depends(get_session), 
                        category_service: CategoryService = Depends(get_category_service)):
    
    return await category_service.get_all(session)
