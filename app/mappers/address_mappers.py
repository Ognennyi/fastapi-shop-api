from app.schemas.address import AddressCreate
from app.models.address import Address as AddressModel




def to_address_model(data: AddressCreate) -> AddressModel:
    address_model = AddressModel(
        country=data.country,
        city=data.city,
        street=data.street,
    )
    return address_model





