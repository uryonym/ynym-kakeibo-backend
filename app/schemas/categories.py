from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str
    seq: int

    model_config = {
        "from_attributes": True,
    }
