from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.seed_title import SeedTitle
from algorithms.nlp.category_loader import get_categories, get_category, force_reload

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db)):
    categories = get_categories()
    result = []
    for cat_id, cat in categories.items():
        # Query seed stats for this category
        seed_count = db.query(func.count(SeedTitle.id)).filter(
            SeedTitle.category == cat_id,
            SeedTitle.is_active == True,
        ).scalar() or 0

        seed_preview = []
        if seed_count > 0:
            preview_seeds = db.query(SeedTitle).filter(
                SeedTitle.category == cat_id,
                SeedTitle.is_active == True,
            ).order_by(SeedTitle.score.desc()).limit(3).all()
            seed_preview = [s.title for s in preview_seeds]

        result.append({
            "id": cat_id,
            "name": cat.get("name", cat_id),
            "icon": cat.get("icon", ""),
            "description": cat.get("description", ""),
            "audience": cat.get("audience", ""),
            "seed_count": seed_count,
            "seed_preview": seed_preview,
        })
    return result


@router.get("/{category_id}/hints")
def category_hints(category_id: str):
    cat = get_category(category_id)
    if not cat:
        return {"error": "分类不存在"}, 404

    return {
        "id": category_id,
        "name": cat.get("name", ""),
        "context_keywords": cat.get("context_keywords", []),
        "hook_patterns": cat.get("hook_patterns", []),
    }


@router.post("/reload")
def reload_categories():
    force_reload()
    return {"status": "ok", "categories_count": len(get_categories())}
