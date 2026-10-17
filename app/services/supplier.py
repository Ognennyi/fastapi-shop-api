from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from app.repositories.address import AddressRepository
from app.repositories.supplier import SupplierRepository

from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierAddressUpdate 

from app.mappers.address_mappers import to_address_model

from app.mappers.supplier_mappers import to_supplier_model, to_supplier_response


from app.core.exceptions import NotFoundError, ConflictError

class SupplierService:

    def __init__(self, rep_supplier: SupplierRepository, rep_address: AddressRepository):
        self.rep_address = rep_address
        self.rep_supplier = rep_supplier


    async def create_supplier(self, session: AsyncSession, data: SupplierCreate) -> SupplierResponse:

        address_model = to_address_model(data.address)  #AddressModel
        created_address = await self.rep_address.create_address(session, address_model) 


        supplier_model = to_supplier_model(data, created_address.id)


        created_supplier = await self.rep_supplier.create_supplier(session, supplier_model)


        supplier_response = to_supplier_response(created_supplier) #SupplierResponse

        await session.commit()
        return supplier_response
    

    async def get_all_supplier(self, session: AsyncSession) -> list[SupplierResponse]:
        suppliers = await self.rep_supplier.get_all(session)
        suppliers_response = [] 
        for supplier in suppliers:
            suppliers_response.append(to_supplier_response(supplier))

        return suppliers_response
    


    async def update_address(self, session: AsyncSession, supplier_id: UUID, new_address: SupplierAddressUpdate):

        supplier = await self.rep_supplier.get_by_id(session, supplier_id)
        if supplier is None:
            raise NotFoundError("Supplier not found")

        new_address = to_address_model(new_address)

        updated_address = await self.rep_address.address_update(session, supplier.address_id, new_address)
        if updated_address is None:
            raise NotFoundError("Address not found") 
        
        await session.commit()

        return updated_address
    

    async def delete_supplier(self, session: AsyncSession, supplier_id: UUID) -> None:
        supplier = await self.rep_supplier.get_by_id(session, supplier_id)
        if supplier is None:
            raise NotFoundError("Supplier not found")
        
        try:
            address_id = supplier.address_id

            await self.rep_supplier.supplier_delete(session, supplier_id)
            await self.rep_address.address_delete(session, address_id)
            await session.commit()


        except IntegrityError:
            await session.rollback()
            raise ConflictError(
                "Supplier cannot be deleted because it has products"
            )
    

    async def get_supplier(self, session: AsyncSession, supplier_id: UUID) -> SupplierResponse:

        supplier = await self.rep_supplier.get_by_id(session, supplier_id)
        if supplier is None:
            raise NotFoundError("Supplier not found")
        
        result_supplier = to_supplier_response(supplier)
        return result_supplier