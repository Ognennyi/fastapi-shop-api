from uuid import UUID

from fastapi import APIRouter, Depends, Query



from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.client import ClientCreate, ClientResponse, ClientAddressUpdate

from app.services.client import ClientService
from app.dependencies import get_client_service

from app.core.exceptions import BadRequestError

from app.schemas.common import ErrorResponse, MessageResponse

router = APIRouter(tags=["Clients"])



@router.post(
    "/clients", 
    response_model=ClientResponse, 
    status_code=201,
    summary="Добавить клиента",
    description="Создаёт нового клиента вместе с его адресом.",
     responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации нового клиента",
        },
    },
)
async def create_client(
                        data: ClientCreate ,
                        session: AsyncSession = Depends(get_session), 
                        client_service: ClientService = Depends(get_client_service)):

    client_response = await client_service.create_client(session, data)

    return client_response





@router.get(
    "/clients",
    response_model=list[ClientResponse],
    status_code=200,
    summary="Получить клиентов",
    description=(
        "Возвращает список клиентов. "
        "Поддерживает поиск по имени и фамилии, а также пагинацию "
        "через limit и offset."
    ),
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Некорректные параметры запроса",
        },
    },
)
async def get_clients(
                        name: str | None = None,
                        surname: str | None = None,
                        limit: int | None = Query(default=None, gt=0),
                        offset: int | None = Query(default=None, ge=0),
                        session: AsyncSession = Depends(get_session),
                        client_service: ClientService = Depends(get_client_service) ):
    

    if (name is None) != (surname is None):
        raise BadRequestError("Name and surname must be provided together")


    if name is not None and surname is not None:
        return await client_service.get_clients_by_name(session, name, surname)

    return await client_service.get_all_clients(session, limit, offset)







@router.delete(
    "/clients/{client_id}",
    response_model=MessageResponse,
    status_code=200,
    summary="Удалить клиента",
    description="Удаляет клиента по его UUID.",
    responses={
        400: {
        "model": ErrorResponse,
        "description": "Некорректный UUID клиента",
        },

        404: {
            "model": ErrorResponse,
            "description": "Клиент не найден",
        },
    },
)
async def delete_client_by_id(
                        client_id: UUID,
                        session: AsyncSession = Depends(get_session), 
                        client_service: ClientService = Depends(get_client_service)):
    
    deleted_client = await client_service.delete_client(session, client_id)

    return {"message": "The client has been deleted."}



@router.patch(
    "/clients/{client_id}/address",
    status_code=200,
    response_model=MessageResponse,
    summary="Изменить адрес клиента",
    description="Заменяет адрес клиента на новый адрес из тела запроса.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации нового адреса",
        },
        404: {
            "model": ErrorResponse,
            "description": "Клиент или его адрес не найден",
        },
    },
)
async def address_update(
                        client_id: UUID ,
                        data: ClientAddressUpdate,
                        session: AsyncSession = Depends(get_session), 
                        client_service: ClientService = Depends(get_client_service)
                        ):
    
    updated_address = await client_service.update_address(session, client_id, data)
    
    return{"message": "The address has been updated."}
 
    
    
