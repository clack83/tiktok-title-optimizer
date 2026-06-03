from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.optimization import OptimizationRecord
from app.schemas.optimization import CompareRequest

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: str | None = None,
    end_date: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(OptimizationRecord).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
    )

    if start_date:
        query = query.filter(OptimizationRecord.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(OptimizationRecord.created_at <= datetime.fromisoformat(end_date))

    total = query.count()
    records = query.order_by(OptimizationRecord.created_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": str(r.id),
                "original_title": r.original_title,
                "results": r.results,
                "scores": r.scores,
                "strategy": r.strategy,
                "category": r.category,
                "created_at": r.created_at.isoformat(),
            }
            for r in records
        ],
    }


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.query(OptimizationRecord).filter(
        OptimizationRecord.id == record_id,
        OptimizationRecord.user_id == current_user.id,
    ).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    record.is_deleted = True
    db.commit()


@router.post("/compare")
def compare_history(
    req: CompareRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    r1 = db.query(OptimizationRecord).filter(
        OptimizationRecord.id == req.record_id_1,
        OptimizationRecord.user_id == current_user.id,
    ).first()
    r2 = db.query(OptimizationRecord).filter(
        OptimizationRecord.id == req.record_id_2,
        OptimizationRecord.user_id == current_user.id,
    ).first()

    if not r1 or not r2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    return {
        "record_1": {
            "id": str(r1.id),
            "original_title": r1.original_title,
            "best_result": r1.results.get("variations", [{}])[0] if r1.results.get("variations") else {},
            "overall_score": r1.scores.get("original_score"),
            "strategy": r1.strategy,
        },
        "record_2": {
            "id": str(r2.id),
            "original_title": r2.original_title,
            "best_result": r2.results.get("variations", [{}])[0] if r2.results.get("variations") else {},
            "overall_score": r2.scores.get("original_score"),
            "strategy": r2.strategy,
        },
    }
