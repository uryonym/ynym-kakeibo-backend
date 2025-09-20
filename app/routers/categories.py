from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.categories import Category
from app.schemas.categories import CategorySchema
from app.db import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategorySchema], summary="カテゴリー一覧取得")
def fetch_categories(db=Depends(get_db)):
    try:
        records = db.query(Category).all()
        if not records:
            return []
        # ORMインスタンスのリストをそのまま返し、FastAPIによるPydantic変換に任せる
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
