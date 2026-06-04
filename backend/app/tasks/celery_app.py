from celery import Celery, Task

from app.core.config import settings

broker_url = settings.redis_url
if broker_url.startswith("rediss://"):
    broker_url = broker_url + "?ssl_cert_reqs=CERT_NONE"

celery_app = Celery(
    "tiktok_optimizer",
    broker=broker_url,
    backend=broker_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_soft_time_limit=600,
)


@celery_app.task(bind=True, name="batch_optimize")
def batch_optimize_task(self: Task, titles: list[str], strategy: str, category: str | None, user_id: str):
    from algorithms.optimizer.pipeline import optimize_title_sync

    results = []
    total = len(titles)

    for i, title in enumerate(titles):
        try:
            result = optimize_title_sync(title, strategy, category)
            results.append({"title": title, "success": True, "result": result})
        except Exception as e:
            results.append({"title": title, "success": False, "error": str(e)})

        self.update_state(
            state="PROGRESS",
            meta={"current": i + 1, "total": total},
        )

    return {"total": total, "results": results}


@celery_app.task(bind=True, name="generate_seeds")
def generate_seeds_task(self: Task, category: str, candidate_count: int = 25, target_count: int = 20):
    """Generate seed titles for a single category."""
    from algorithms.nlp.seed_generator import generate_seeds
    from app.models.seed_title import SeedTitle
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        # Deactivate old seeds
        db.query(SeedTitle).filter(SeedTitle.category == category).update({"is_active": False})
        db.commit()

        # Generate new seeds
        seeds = generate_seeds(category, candidate_count, target_count)
        for s in seeds:
            record = SeedTitle(
                category=category,
                title=s["title"],
                score=s["score"],
                hook_type=s["hook_type"],
                is_active=True,
            )
            db.add(record)
        db.commit()

        return {"category": category, "generated_count": len(seeds), "status": "success"}
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="refresh_all_seeds")
def refresh_all_seeds_task(self: Task):
    """Coordinator task: trigger seed generation for all categories in parallel."""
    from algorithms.nlp.category_loader import get_category_ids

    category_ids = get_category_ids()
    results = []

    for cat_id in category_ids:
        task = generate_seeds_task.delay(cat_id)
        results.append({"category": cat_id, "task_id": task.id})

    return {"total_categories": len(category_ids), "tasks": results}


celery_app.conf.beat_schedule = {
    "refresh-seeds-weekly": {
        "task": "refresh_all_seeds",
        "schedule": 604800.0,  # 7 days in seconds
    },
}
