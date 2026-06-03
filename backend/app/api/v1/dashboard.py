from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.optimization import OptimizationRecord
from app.core.redis_client import cache_get, cache_set

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
async def overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cache_key = f"dashboard:overview:{current_user.id}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    total = db.query(func.count(OptimizationRecord.id)).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
    ).scalar() or 0

    records = db.query(OptimizationRecord).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
    ).all()

    avg_improvement = 0.0
    strategies = Counter()
    for r in records:
        variations = r.results.get("variations", [])
        if variations:
            for v in variations:
                delta = v.get("score_delta", 0)
                avg_improvement += delta
                break
        strategies[r.strategy or "auto"] += 1

    if total > 0:
        avg_improvement = round(avg_improvement / total, 1)

    result = {
        "total_optimizations": total,
        "avg_score_improvement": avg_improvement,
        "top_strategies": strategies.most_common(5),
    }

    await cache_set(cache_key, result, ttl=300)
    return result


@router.get("/trends")
async def trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)

    records = db.query(OptimizationRecord).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
        OptimizationRecord.created_at >= since,
    ).order_by(OptimizationRecord.created_at.asc()).all()

    daily_data: dict[str, list[float]] = {}
    for r in records:
        day = r.created_at.strftime("%Y-%m-%d")
        if day not in daily_data:
            daily_data[day] = []
        daily_data[day].append(float(r.scores.get("original_score", 0)))

    trend = []
    for day in sorted(daily_data.keys()):
        scores = daily_data[day]
        trend.append({
            "date": day,
            "avg_score": round(sum(scores) / len(scores), 1),
            "count": len(scores),
        })

    return {"trend": trend}


@router.get("/keywords-cloud")
async def keywords_cloud(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cache_key = f"dashboard:keywords:{current_user.id}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    records = db.query(OptimizationRecord.original_title).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
    ).all()

    import jieba
    word_counter = Counter()
    for (title,) in records:
        words = jieba.lcut(title)
        for w in words:
            if len(w.strip()) >= 2:
                word_counter[w] += 1

    top_words = [{"word": w, "count": c} for w, c in word_counter.most_common(50)]

    await cache_set(cache_key, {"keywords": top_words}, ttl=300)
    return {"keywords": top_words}


@router.get("/score-distribution")
async def score_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = db.query(OptimizationRecord.scores).filter(
        OptimizationRecord.user_id == current_user.id,
        OptimizationRecord.is_deleted == False,
    ).all()

    buckets = {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0}
    for (scores,) in records:
        s = scores.get("original_score", 0) if scores else 0
        if s < 20:
            buckets["0-20"] += 1
        elif s < 40:
            buckets["20-40"] += 1
        elif s < 60:
            buckets["40-60"] += 1
        elif s < 80:
            buckets["60-80"] += 1
        else:
            buckets["80-100"] += 1

    return {"distribution": [{"range": k, "count": v} for k, v in buckets.items()]}
