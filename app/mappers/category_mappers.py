


from app.schemas.category import CategoryCreate, CategoryResponse
from app.models.category import Category



def to_category_model(data: CategoryCreate) -> Category:
    return Category(
        name = data.name
    )


def to_category_response(data: Category) -> CategoryResponse:
    return CategoryResponse(
        id = data.id,
        name = data.name
    )