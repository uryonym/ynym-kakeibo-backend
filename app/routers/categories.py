from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

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


@router.get("/get", response_model=CategorySchema, summary="カテゴリー単体取得")
def fetch_category(id: UUID, db=Depends(get_db)):
    """クエリパラメーター `id` を受け取り、該当するカテゴリを返す。

    - 存在しない場合は 404 を返す
    - DB/検索エラーは 500 を返す
    """
    try:
        # SQLAlchemy 2 系推奨の Session.get を使用して主キーで取得
        record = db.get(Category, id)
        if not record:
            # 見つからない場合は 404 を返す
            raise HTTPException(status_code=404, detail="カテゴリーが見つかりません")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete", summary="カテゴリー削除", status_code=204)
def delete_category(id: UUID, db=Depends(get_db)):
    """クエリパラメーター `id` を受け取り、該当するカテゴリを削除する。

    - 存在しない場合は 404 を返す
    - 成功時は 204 No Content を返す
    - DB エラーは 500 を返す
    """
    try:
        record = db.get(Category, id)
        if not record:
            raise HTTPException(status_code=404, detail="カテゴリーが見つかりません")
        # 削除してコミット
        db.delete(record)
        db.commit()
        # 204 を返すために何も返さない
        return None
    except HTTPException:
        raise
    except Exception as e:
        # 何らかの DB エラー等が起きた場合はロールバックして 500
        try:
            db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))
