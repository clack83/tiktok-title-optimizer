from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.optimization import OptimizationRecord
from app.schemas.optimization import (
    OptimizeRequest, ScoreRequest, KeywordsRequest,
    BatchOptimizeRequest,
)
from algorithms.scoring import create_scoring_engine
from algorithms.optimizer.pipeline import optimize_title
from algorithms.nlp.keyword_extractor import extract_keywords
from algorithms.nlp.topic_matcher import match_topics

router = APIRouter(prefix="/optimize", tags=["optimize"])

scoring_engine = create_scoring_engine()


@router.post("")
async def optimize(req: OptimizeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = await optimize_title(req.title, req.strategy, req.category, req.count)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    # Save history
    record_data: dict = {
        "variations": result["variations"],
    }
    if result.get("seeds_used"):
        record_data["seeds_used"] = result["seeds_used"]
    if result.get("warnings"):
        record_data["warnings"] = result["warnings"]

    record = OptimizationRecord(
        user_id=current_user.id,
        original_title=req.title,
        results=record_data,
        scores={"original_score": result["original_score"]},
        strategy=req.strategy,
        category=req.category,
    )
    db.add(record)
    db.commit()

    result["record_id"] = str(record.id)
    return result


@router.post("/score")
def score(req: ScoreRequest):
    try:
        result = scoring_engine.evaluate(req.title)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return {
        "title": req.title,
        "overall_score": result.overall_score,
        "dimension_scores": result.dimension_scores,
        "explanations": result.explanations,
    }


@router.post("/keywords")
def keywords(req: KeywordsRequest):
    kw = extract_keywords(req.title)
    topics = match_topics(kw)
    return {
        "title": req.title,
        "keywords": kw,
        "matched_topics": topics,
    }


@router.post("/batch")
async def batch_optimize(
    req: BatchOptimizeRequest,
    current_user: User = Depends(get_current_user),
):
    from app.tasks.celery_app import batch_optimize_task
    task = batch_optimize_task.delay(
        titles=req.titles,
        strategy=req.strategy,
        category=req.category,
        user_id=str(current_user.id),
    )
    return {"task_id": task.id, "total": len(req.titles)}


@router.get("/batch/{task_id}")
def batch_status(task_id: str):
    from celery.result import AsyncResult
    from app.tasks.celery_app import celery_app

    result = AsyncResult(task_id, app=celery_app)
    response = {"task_id": task_id, "status": result.state}

    if result.state == "PROGRESS":
        response["progress"] = result.info
    elif result.state == "SUCCESS":
        response["result"] = result.result
    elif result.state == "FAILURE":
        response["error"] = str(result.info)

    return response
