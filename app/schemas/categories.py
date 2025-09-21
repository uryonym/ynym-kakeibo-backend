from __future__ import annotations

import uuid
from pydantic import BaseModel


class CategorySchema(BaseModel):
    # DB 側の UUID を Python 側では uuid.UUID として扱う
    id: uuid.UUID
    name: str
    seq: int

    model_config = {
        # SQLAlchemy ORM インスタンスの属性からの変換を許可
        "from_attributes": True,
    }
