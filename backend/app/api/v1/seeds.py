from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.redis_client import cache_get, cache_set
from app.models.user import User
from app.models.seed_title import SeedTitle
from app.schemas.seed import SeedRefreshRequest, SeedRefreshResponse
from algorithms.nlp.category_loader import get_category_ids
from algorithms.nlp.seed_generator import generate_seeds

router = APIRouter(prefix="/seeds", tags=["seeds"])


@router.get("")
async def list_seeds(category: str | None = Query(None), db: Session = Depends(get_db)):
    cache_key = f"seeds:{category or 'all'}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    if category:
        seeds = db.query(SeedTitle).filter(
            SeedTitle.category == category,
            SeedTitle.is_active == True,
        ).order_by(SeedTitle.score.desc()).limit(20).all()
        result = [
            {"id": str(s.id), "title": s.title, "score": s.score, "hook_type": s.hook_type, "generated_at": s.generated_at.isoformat()}
            for s in seeds
        ]
    else:
        cat_ids = get_category_ids()
        result = {}
        for cid in cat_ids:
            seeds = db.query(SeedTitle).filter(
                SeedTitle.category == cid,
                SeedTitle.is_active == True,
            ).order_by(SeedTitle.score.desc()).limit(5).all()
            result[cid] = [
                {"id": str(s.id), "title": s.title, "score": s.score, "hook_type": s.hook_type, "generated_at": s.generated_at.isoformat()}
                for s in seeds
            ]

    await cache_set(cache_key, result, ttl=300)
    return result


@router.post("/refresh")
async def refresh_seeds(req: SeedRefreshRequest, db: Session = Depends(get_db)):
    categories_to_refresh = [req.category] if req.category else get_category_ids()
    results = []

    for cat in categories_to_refresh:
        try:
            # Deactivate old seeds
            db.query(SeedTitle).filter(SeedTitle.category == cat).update({"is_active": False})
            db.commit()

            # Generate new seeds
            seeds = generate_seeds(cat)
            for s in seeds:
                record = SeedTitle(
                    category=cat,
                    title=s["title"],
                    score=s["score"],
                    hook_type=s["hook_type"],
                    is_active=True,
                )
                db.add(record)
            db.commit()

            results.append({"category": cat, "generated_count": len(seeds), "status": "success"})
        except Exception as e:
            db.rollback()
            results.append({"category": cat, "generated_count": 0, "status": "failed", "error": str(e)})

    return {"results": results}
