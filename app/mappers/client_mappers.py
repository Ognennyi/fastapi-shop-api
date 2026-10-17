from app.schemas.client import ClientCreate, ClientResponse
from app.models.client import Client as ClientModel




def to_client_model(data: ClientCreate, created_address_id) -> ClientModel:

    client_model = ClientModel(
        client_name = data.client_name,
        client_surname = data.client_surname,
        birthday = data.birthday,
        gender = data.gender,
        address_id = created_address_id
    )
    return client_model



def to_client_response(data: ClientModel) -> ClientResponse:
    client_response = ClientResponse(
        id = data.id,
        client_name = data.client_name,
        client_surname = data.client_surname,
        birthday = data.birthday,
        gender = data.gender,
        registration_date = data.registration_date,
        address_id = data.address_id
    )

    return client_response

