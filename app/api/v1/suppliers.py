from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session


from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierAddressUpdate 

from app.services.supplier import SupplierService
from app.dependencies import get_supplier_service

from app.schemas.common import ErrorResponse, MessageResponse

router = APIRouter(tags=["Suppliers"])



@router.post(
    "/suppliers",
    response_model=SupplierResponse,
    status_code=201,
    summary="Добавить поставщика",
    description="Создаёт нового поставщика вместе с его адресом.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации данных поставщика",
        },
    },
)
async def create_supplier(
                        data: SupplierCreate ,
                        session: AsyncSession = Depends(get_session), 
                        supplier_service: SupplierService = Depends(get_supplier_service)
    ):
    
    supplier_response = await supplier_service.create_supplier(session, data)

    return supplier_response





@router.get(
    "/suppliers",
    response_model=list[SupplierResponse],
    status_code=200,
    summary="Получить всех поставщиков",
    description=(
        "Возвращает список всех поставщиков. "
        "Если поставщиков нет, возвращается пустой список."
    ),
)
async def get_all_suppliers(
                        session: AsyncSession = Depends(get_session), 
                        supplier_service: SupplierService = Depends(get_supplier_service)
                        ):
    
    all_suppliers = await supplier_service.get_all_supplier(session)

    return all_suppliers






@router.patch(
    "/suppliers/{supplier_id}/address",
    response_model=MessageResponse,
    status_code=200,
    summary="Изменить адрес поставщика",
    description="Заменяет адрес поставщика на новый адрес из тела запроса.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID или ошибка валидации нового адреса",
        },
        404: {
            "model": ErrorResponse,
            "description": "Поставщик или его адрес не найден",
        },
    },
)
async def address_update(
                        supplier_id: UUID ,
                        data: SupplierAddressUpdate,
                        session: AsyncSession = Depends(get_session), 
                        supplier_service: SupplierService = Depends(get_supplier_service)
                        ):
    
    updated_address = await supplier_service.update_address(session, supplier_id, data)
    
    return{"message": "The address has been updated."}    






@router.delete(
    "/suppliers/{supplier_id}",
    response_model=MessageResponse,
    status_code=200,
    summary="Удалить поставщика",
    description="Удаляет поставщика по его UUID.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID поставщика",
        },
        404: {
            "model": ErrorResponse,
            "description": "Поставщик не найден",
        },
        409: {
            "model": ErrorResponse,
            "description": "Поставщик связан с существующими товарами",
        },
    },
)
async def delete_supplier_by_id(
                        supplier_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        supplier_service: SupplierService = Depends(get_supplier_service)):
    
    await supplier_service.delete_supplier(session, supplier_id)

    return {"message": "The supplier has been deleted."}





@router.get(
    "/suppliers/{supplier_id}",
    response_model=SupplierResponse,
    status_code=200,
    summary="Получить поставщика по ID",
    description="Возвращает поставщика по его UUID.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректный UUID поставщика",
        },
        404: {
            "model": ErrorResponse,
            "description": "Поставщик не найден",
        },
    },
)
async def get_supplier_by_id(
                        supplier_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        supplier_service: SupplierService = Depends(get_supplier_service)
                        ):
    find_supplier = await supplier_service.get_supplier(session, supplier_id)
    
    return find_supplier






# Для поставщиков:

# Добавление поставщика (на вход подается json, соответствующей структуре, описанной сверху).  DONE

# Изменение адреса поставщика 
# (параметры: id и новый адрес в виде json в соответствии с выше описанным форматом).  DONE

# Удаление поставщика по id      DONE

# Получение всех поставщиков   DONE

# Получение поставщика по id      DONE