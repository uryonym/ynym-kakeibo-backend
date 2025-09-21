from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.models.categories import Category
from app.schemas.categories import CategorySchema, CategoryEdit
from uuid import uuid4
from fastapi import status
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


@router.get("/{id}", response_model=CategorySchema, summary="カテゴリー単体取得")
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


@router.post(
    "/",
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED,
    summary="カテゴリー作成",
)
def create_category(payload: CategoryEdit, db=Depends(get_db)):
    """新しいカテゴリを作成する

    - 成功時は 201 と作成したリソースを返す
    - DB エラーは 500 を返す
    """
    try:
        new_id = uuid4()
        category = Category(id=new_id, name=payload.name, seq=payload.seq)
        db.add(category)
        db.commit()
        # commit 後に最新の状態を返すために refresh
        db.refresh(category)
        return category
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}", response_model=CategorySchema, summary="カテゴリー更新")
def update_category(id: UUID, payload: CategoryEdit, db=Depends(get_db)):
    """指定した ID のカテゴリを更新する

    - 存在しない場合は 404 を返す
    - 成功時は更新後のオブジェクトを返す
    - DB エラーは 500 を返す
    """
    try:
        record = db.get(Category, id)
        if not record:
            raise HTTPException(status_code=404, detail="カテゴリーが見つかりません")

        # 部分更新を適用
        record.name = payload.name
        record.seq = payload.seq

        db.commit()
        db.refresh(record)
        return record
    except HTTPException:
        raise
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", summary="カテゴリー削除", status_code=204)
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
