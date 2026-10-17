from uuid import UUID

from fastapi import Body
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session




from app.services.image import ImageService
from app.dependencies import get_image_service

from app.schemas.product import ProductResponse

from app.schemas.common import ErrorResponse, MessageResponse


router = APIRouter(tags=["Images"])




@router.post(
    "/products/{product_id}/image",
    response_model=ProductResponse,
    status_code=201,
    summary="Добавить изображение товару",
    description=(
        "Добавляет бинарное изображение товару. "
        "Тело запроса передаётся в формате application/octet-stream."
    ),
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID товара или пустое тело запроса",
        },
        404: {
            "model": ErrorResponse,
            "description": "Товар не найден",
        },
        409: {
            "model": ErrorResponse,
            "description": "У товара уже есть изображение",
        },
    },
)
async def create_image(
                        product_id: UUID,
                        image_bytes: bytes = Body(media_type="application/octet-stream"),
                        session: AsyncSession = Depends(get_session), 
                        image_service: ImageService = Depends(get_image_service)
                        ):
    created_image = await image_service.create_image(session, product_id, image_bytes)
    
    return created_image




@router.get(
    "/images/{image_id}",
    response_class=Response,
    status_code=200,
    summary="Получить изображение по ID",
    description=(
        "Возвращает бинарные данные изображения. "
        "Файл передаётся как application/octet-stream и предлагается для скачивания."
    ),
    responses={
        200: {
            "description": "Бинарный файл изображения",
            "content": {
                "application/octet-stream": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            },
            "headers": {
                "Content-Disposition": {
                    "description": "Указывает браузеру скачать файл",
                    "schema": {
                        "type": "string",
                    },
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID изображения",
        },
        404: {
            "model": ErrorResponse,
            "description": "Изображение не найдено",
        },
    },
)
async def get_image_by_id(
                        image_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        image_service: ImageService = Depends(get_image_service)):
    
    find_image = await image_service.get_image_by_id(session, image_id)

    return Response(
        content = find_image.image,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": 'attachment; filename="image.bin"'
        }
    )





@router.get(
    "/products/{product_id}/image",
    response_class=Response,
    status_code=200,
    summary="Получить изображение товара",
    description=(
        "Возвращает изображение, связанное с указанным товаром. "
        "Файл передаётся как application/octet-stream."
    ),
    responses={
        200: {
            "description": "Бинарный файл изображения",
            "content": {
                "application/octet-stream": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            },
            "headers": {
                "Content-Disposition": {
                    "description": "Указывает браузеру скачать файл",
                    "schema": {
                        "type": "string",
                    },
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID товара",
        },
        404: {
            "model": ErrorResponse,
            "description": "Товар или его изображение не найдены",
        },
    },
)
async def get_image_by_product_id(
                        product_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        image_service: ImageService = Depends(get_image_service)):
    
    find_image = await image_service.get_image_by_product_id(session, product_id)

    return Response(
        content = find_image.image,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": 'attachment; filename="image.bin"'
        }
    )


@router.delete(
    "/images/{image_id}",
    response_model=MessageResponse,
    status_code=200,
    summary="Удалить изображение",
    description="Удаляет изображение по его UUID.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID изображения",
        },
        404: {
            "model": ErrorResponse,
            "description": "Изображение не найдено",
        },
    },
)
async def delete_image_by_id(
                        image_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        image_service: ImageService = Depends(get_image_service)):
    
    deleted_image = await image_service.delete_image(session, image_id)

    return {"message": "The image has been deleted."}







@router.put(
    "/images/{image_id}",
    response_model=MessageResponse,
    status_code=200,
    summary="Заменить изображение",
    description=(
        "Полностью заменяет бинарные данные существующего изображения. "
        "Новое изображение передаётся как application/octet-stream."
    ),
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID изображения или пустое тело запроса",
        },
        404: {
            "model": ErrorResponse,
            "description": "Изображение не найдено",
        },
    },
)
async def image_update(
                        image_id: UUID,
                        image_bytes: bytes = Body(media_type="application/octet-stream"),
                        session: AsyncSession = Depends(get_session), 
                        image_service: ImageService = Depends(get_image_service)
                        ):
    
    updated_image = await image_service.update_image(session, image_id, image_bytes)
    
    return{"message": "The image has been updated."}






