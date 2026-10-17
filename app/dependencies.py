from app.repositories.address import AddressRepository


from app.repositories.client import ClientRepository
from app.services.client import ClientService

from app.repositories.supplier import SupplierRepository
from app.services.supplier import SupplierService


from app.repositories.product import ProductRepository
from app.services.product import ProductService

from app.repositories.image import ImageRepository
from app.repositories.category import CategoryRepository


from app.services.category import CategoryService


from app.services.image import ImageService


def get_client_service() -> ClientService:
    return ClientService(
        rep_address=AddressRepository(),
        rep_client=ClientRepository(),
    )

def get_supplier_service() -> SupplierService:
    return SupplierService(
        rep_supplier=SupplierRepository(),
        rep_address=AddressRepository(),
    )


def get_product_service() -> ProductService:
    return ProductService(
        rep_product = ProductRepository(),
        rep_category = CategoryRepository(),
        rep_image = ImageRepository(),
        rep_supplier= SupplierRepository()
    )


def get_category_service() -> CategoryService:
    return CategoryService(
        rep_category = CategoryRepository()
    )



def get_image_service() -> ImageService:
    return ImageService(
        rep_image = ImageRepository(),
        rep_product = ProductRepository()
    )