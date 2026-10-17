from app.schemas.supplier import SupplierCreate, SupplierResponse
from app.models.supplier import Supplier as SupplierModel




def to_supplier_model(data: SupplierCreate, created_address_id) -> SupplierModel:

    supplier_model = SupplierModel(
        name = data.name,
        phone_number = data.phone_number,
        address_id = created_address_id,
    )

    return supplier_model


def to_supplier_response(data: SupplierModel) -> SupplierResponse:

    supplier_response = SupplierResponse(
        id = data.id,
        name = data.name,
        phone_number = data.phone_number,
        address_id = data.address_id
    )

    return supplier_response

