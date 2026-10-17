
from app.models.image import Image


def to_image_model(image_bytes: bytes) -> Image:

    return Image(image=image_bytes)

