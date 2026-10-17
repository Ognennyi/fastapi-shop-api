from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.supplier import Supplier
from sqlalchemy import select, delete

class SupplierRepository:

    async def create_supplier(self, session: AsyncSession, supplier: Supplier) -> Supplier:
        session.add(supplier)
        await session.flush()
        await session.refresh(supplier)
        return supplier 
    
    async def get_by_id(self, session: AsyncSession, supplier_id: UUID) -> Supplier | None:
        find_supplier = select(Supplier).where(Supplier.id == supplier_id)
        result = await session.scalar(find_supplier)

        if result is None:
            return None
        return result
    
    async def get_all(self, session: AsyncSession) -> list[Supplier]:
        suppliers = select(Supplier)
        request = await session.scalars(suppliers)
        request = request.all()
        return request
    
    async def supplier_delete(self, session: AsyncSession, supplier_id:UUID) -> bool:
        del_supplier = delete(Supplier).where(Supplier.id == supplier_id)
        result_response = await session.execute(del_supplier) 
        return result_response.rowcount > 0 


# Для поставщиков:

#Done
# Добавление поставщика (на вход подается json, соответствующей структуре, описанной сверху).

# Изменение адреса поставщика (параметры: id и новый адрес в виде json в соответствии с выше описанным форматом).

#Done
# Удаление поставщика по id

#Done
# Получение всех поставщиков

#Done
# Получение поставщика по id