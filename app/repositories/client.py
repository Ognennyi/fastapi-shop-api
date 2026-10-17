from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.client import Client
from sqlalchemy import select, and_, delete

class ClientRepository:

    async def create_client(self, session: AsyncSession, client: Client) -> Client:
        session.add(client)
        await session.flush()
        await session.refresh(client)
        return client
    
    
    async def get_by_id(self, session: AsyncSession, client_id: UUID) -> Client | None:
        find_client = select(Client).where(Client.id == client_id)
        result = await session.scalar(find_client)
        if result is None:
            return None
        return result



    async def get_by_name_and_surname(self, session: AsyncSession, name:str, surname:str) -> list[Client]:

        clients = select(Client).where( and_(Client.client_name == name, Client.client_surname == surname))
        request = await session.scalars(clients)
        request = request.all()
        return request
    

    async def get_all(self, session: AsyncSession, limit:int | None, offset:int | None) -> list[Client]:

        clients = select(Client)
        if limit is not None:
            clients = clients.limit(limit)
        if offset is not None:
            clients = clients.offset(offset)
        request = await session.scalars(clients)
        request = request.all()
        return request


    async def client_delete(self, session: AsyncSession, client_id:UUID) -> bool:
    
        del_client = delete(Client).where(Client.id == client_id)
        result_response = await session.execute(del_client) 
        return result_response.rowcount > 0 
    







# Для клиентов:

#Done
# Добавление клиента (на вход подается json, соответствующей структуре, описанной сверху). 

#Done
# Удаление клиента (по его идентификатору). 

#Done
# Получение клиентов по имени и фамилии (параметры — имя и фамилия). 

#Done
# Получение всех клиентов 
# (В данном запросе необходимо предусмотреть опциональные параметры пагинации в строке запроса: limit и offset).  
# В случае отсутствия этих параметров возвращать весь список. 


# Изменение адреса клиента (параметры: id и новый адрес в виде json в соответствии с выше описанным форматом).



