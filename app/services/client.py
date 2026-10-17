from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.client import ClientCreate, ClientAddressUpdate, ClientResponse


from app.repositories.address import AddressRepository
from app.repositories.client import ClientRepository


from app.mappers.address_mappers import to_address_model

from app.mappers.client_mappers import to_client_model, to_client_response

from app.core.exceptions import NotFoundError

class ClientService:

    def __init__(self, rep_address: AddressRepository, rep_client: ClientRepository):
        self.rep_address = rep_address
        self.rep_client = rep_client

    async def create_client(self, session: AsyncSession, data:ClientCreate) -> ClientResponse:

        address_model = to_address_model(data.address)  #AddressModel
        created_address = await self.rep_address.create_address(session,address_model) 


        client_model = to_client_model(data, created_address.id)

        created_client = await self.rep_client.create_client(session, client_model)

        client_response = to_client_response(created_client) #ClientResponse

        await session.commit()
        return client_response
    


    async def get_all_clients(self, session: AsyncSession, limit: int | None, offset: int | None) -> list[ClientResponse]:
        clients = await self.rep_client.get_all(session, limit, offset)
        clients_response = [] 
        for client in clients:
            clients_response.append(to_client_response(client))

        return clients_response

    async def get_clients_by_name(self, session: AsyncSession, name: str, surname: str) -> list[ClientResponse]:


        clients = await self.rep_client.get_by_name_and_surname(session, name, surname)
        
        clients_response = []
        for client in clients:
            clients_response.append(to_client_response(client))

        return clients_response


    async def delete_client(self, session: AsyncSession, client_id: UUID) -> bool:
        client = await self.rep_client.get_by_id(session, client_id)

        if client is None:
            raise NotFoundError("Client not found")
        
        address_id = client.address_id


        deleted_client = await self.rep_client.client_delete(session, client_id)

        await self.rep_address.address_delete(session, address_id)

        await session.commit()
        return deleted_client


    async def update_address(self, session: AsyncSession, client_id: UUID, new_address: ClientAddressUpdate):

        client = await self.rep_client.get_by_id(session, client_id)
        if client is None:
            raise NotFoundError("Client not found")

        new_address = to_address_model(new_address)

        updated_address = await self.rep_address.address_update(session, client.address_id, new_address)
        if updated_address is None:
            raise NotFoundError("Address not found")
        
        await session.commit()

        return updated_address




        

        







# получил ClientCreate
# ↓
# преобразовал data.address через mapper в Address ORM
# ↓
# AddressRepository.create_address()
# ↓
# получил address.id
# ↓
# преобразовал ClientCreate + address.id в Client ORM
# ↓
# ClientRepository.create()
# ↓
# commit
# ↓
# преобразовал Client ORM в ClientResponse
# ↓
# вернул Router