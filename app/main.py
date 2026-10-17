from fastapi import FastAPI

from app.api.v1.clients import router as clients_router
from app.api.v1.suppliers import router as supplier_router


from app.api.v1.categories import router as category_router
from app.api.v1.products import router as product_router
from app.api.v1.images import router as image_router


import app.models # register SQLAlchemy models

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.core.exceptions import NotFoundError, BadRequestError, ConflictError

from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title="ShopAPI",
    description="REST API магазина бытовой техники",
    version="1.0.0",
    debug=True,
    docs_url="/swagger/index.html",
    openapi_url="/swagger/openapi.json",
)




@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(BadRequestError)
async def bad_request_handler(request, exc: BadRequestError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(ConflictError)
async def conflict_handler(request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request data",
            "errors": jsonable_encoder(exc.errors()),
        },
    )




@app.get("/", include_in_schema=False)
async def root():
    return{"message" : "ShopAPI works"}


app.include_router(
    clients_router,
    prefix="/api/v1"
)

app.include_router(
    supplier_router, 
    prefix="/api/v1"
)

app.include_router(
    product_router, 
    prefix="/api/v1"
)

app.include_router(
    category_router, 
    prefix="/api/v1"
)

app.include_router(
    image_router, 
    prefix="/api/v1"
)



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict):
                responses = operation.get("responses")

                if responses is not None:
                    responses.pop("422", None)

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi