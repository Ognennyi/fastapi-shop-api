from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.address import Address
from sqlalchemy import select, delete


class AddressRepository:

    async def create_address(self, session: AsyncSession, address: Address) -> Address:
        session.add(address)
        await session.flush()
        await session.refresh(address)
        return address
    
    async def get_by_id(self, session: AsyncSession, address_id: UUID) -> Address | None:
        find_address = select(Address).where(Address.id == address_id)
        result = await session.scalar(find_address)

        if result is None:
            return None
        return result
    
    
    async def address_update(self, session: AsyncSession, address_id:UUID, new_address: Address) -> Address | None:
        address = await session.get(Address, address_id)

        if address is None:
            return None
        
        address.country = new_address.country
        address.city = new_address.city
        address.street = new_address.street

        await session.flush()
        return address
    

    async def address_delete(self, session: AsyncSession, address_id: UUID) -> bool:
        result = await session.execute(delete(Address).where(Address.id == address_id))
        return result.rowcount > 0