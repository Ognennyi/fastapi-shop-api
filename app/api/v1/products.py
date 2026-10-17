from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session


from app.schemas.product import ProductCreate, ProductResponse, ProductStockUpdate


from app.services.product import ProductService
from app.dependencies import get_product_service

from app.schemas.common import ErrorResponse, MessageResponse

router = APIRouter(tags=["Products"])



@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201,
    summary="Добавить товар",
    description="Создаёт новый товар с указанной категорией и поставщиком.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации данных товара",
        },
        404: {
            "model": ErrorResponse,
            "description": "Категория или поставщик не найдены",
        },
    },
)
async def create_product(
                        data: ProductCreate ,
                        session: AsyncSession = Depends(get_session), 
                        product_service: ProductService = Depends(get_product_service)
    ):
    
    return await product_service.create_product(session, data)

    


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=200,
    summary="Получить товар по ID",
    description="Возвращает товар по его UUID.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID товара",
        },
        404: {
            "model": ErrorResponse,
            "description": "Товар не найден",
        },
    },
)
async def get_product_by_id(
                        product_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        product_service: ProductService = Depends(get_product_service)):
    
    find_product = await product_service.get_by_id(session, product_id)


    return find_product





@router.get(
    "/products",
    response_model=list[ProductResponse],
    status_code=200,
    summary="Получить доступные товары",
    description=(
        "Возвращает список товаров, количество которых на складе больше нуля. "
        "Если доступных товаров нет, возвращается пустой список."
    ),
)
async def get_all_product(
                        session: AsyncSession = Depends(get_session), 
                        product_service: ProductService = Depends(get_product_service)):
    
    all_products = await product_service.get_all_products(session)

    return all_products




@router.delete(
    "/products/{product_id}",
    response_model=MessageResponse,
    status_code=200,
    summary="Удалить товар",
    description="Удаляет товар по его UUID.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID товара",
        },
        404: {
            "model": ErrorResponse,
            "description": "Товар не найден",
        },
    },
)
async def delete_product_by_id(
                        product_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        product_service: ProductService = Depends(get_product_service)):
    
    deleted_product = await product_service.delete_product(session, product_id)

    return {"message": "The product has been deleted."}




@router.patch(
    "/products/{product_id}/stock",
    response_model=ProductResponse,
    status_code=200,
    summary="Уменьшить количество товара",
    description=(
        "Уменьшает количество товара на складе на значение amount "
        "из тела запроса."
    ),
    responses={
        400: {
            "model": ErrorResponse,
            "description": (
                "Некорректный UUID, некорректное amount "
                "или недостаточное количество товара"
            ),
        },
        404: {
            "model": ErrorResponse,
            "description": "Товар не найден",
        },
    },
)
async def product_update(
                        product_id: UUID ,
                        data: ProductStockUpdate,
                        session: AsyncSession = Depends(get_session), 
                        product_service: ProductService = Depends(get_product_service)
                        ):
    
    new_stock = await product_service.deacrease_stock(session, product_id, data.amount)

    return new_stock


