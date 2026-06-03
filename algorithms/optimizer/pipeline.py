import hashlib
import json
import logging
from typing import Any

from algorithms.optimizer.deepseek_client import deepseek_client
from algorithms.optimizer.strategies import (
    STRATEGY_PROMPTS,
    OPTIMIZATION_SYSTEM_PROMPT,
    OPTIMIZATION_USER_PROMPT,
    REFERENCE_SEEDS_SECTION,
)
from algorithms.scoring import create_scoring_engine
from algorithms.nlp.seed_generator import select_fewshot_seeds
from app.core.redis_client import cache_get, cache_set

logger = logging.getLogger(__name__)

scoring_engine = create_scoring_engine()


def _validate_category(category: str | None) -> None:
    if not category:
        return
    from algorithms.nlp.category_loader import get_category_ids
    valid_ids = get_category_ids()
    if category not in valid_ids:
        raise ValueError(f"不支持该分类，可选分类：{', '.join(valid_ids)}")


def _build_category_context(category: str | None) -> str:
    if not category:
        return ""
    from algorithms.nlp.category_loader import get_category_context
    ctx = get_category_context(category)
    return ctx if ctx else ""


def _cache_key(title: str, strategy: str, category: str | None) -> str:
    raw = f"{title}|{strategy}|{category or ''}"
    return f"optimize:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def _get_seed_titles(category: str | None, user_title: str) -> tuple[list[dict], list[str]]:
    """Fetch active seeds for the category and select few-shot examples.
    Returns (selected_seeds, seed_ids_used).
    """
    if not category:
        return [], []

    from app.models.seed_title import SeedTitle
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        seeds = db.query(SeedTitle).filter(
            SeedTitle.category == category,
            SeedTitle.is_active == True,
        ).order_by(SeedTitle.score.desc()).all()

        if not seeds:
            return [], []

        seed_dicts = [
            {"title": s.title, "score": s.score, "hook_type": s.hook_type, "id": str(s.id)}
            for s in seeds
        ]

        selected = select_fewshot_seeds(user_title, category, seed_dicts, top_n=5)
        seed_ids = [s["id"] for s in selected]
        return selected, seed_ids
    finally:
        db.close()


async def optimize_title(
    title: str,
    strategy: str = "auto",
    category: str | None = None,
    count: int = 4,
) -> dict[str, Any]:
    if not title.strip():
        raise ValueError("标题不能为空")

    _validate_category(category)

    # Check cache
    ck = _cache_key(title, strategy, category)
    cached = await cache_get(ck)
    if cached:
        return cached

    # Score original
    original_score = scoring_engine.evaluate(title)

    # Build prompts
    strategy_text = STRATEGY_PROMPTS.get(strategy, STRATEGY_PROMPTS["auto"])
    category_text = _build_category_context(category)

    # Fetch few-shot seeds
    selected_seeds, seeds_used = _get_seed_titles(category, title)
    reference_seeds_text = ""
    warnings: list[str] = []
    if selected_seeds:
        seed_lines = "\n".join(
            f"- [{s['hook_type']}] {s['title']} (评分: {s['score']})"
            for s in selected_seeds
        )
        reference_seeds_text = REFERENCE_SEEDS_SECTION.format(seed_titles=seed_lines)
    elif category:
        warnings.append(f"分类 '{category}' 暂无可用种子标题，使用常规优化模式")

    system_prompt = OPTIMIZATION_SYSTEM_PROMPT.format(
        strategy_instruction=strategy_text,
        category_context=category_text,
    )
    user_prompt = OPTIMIZATION_USER_PROMPT.format(
        original_title=title,
        reference_seeds=reference_seeds_text,
        count=count,
    )

    # Call DeepSeek
    try:
        result = deepseek_client.chat_completion(system_prompt, user_prompt)
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise

    # Score each optimized title
    variations = result.get("variations", [])
    for var in variations:
        try:
            opt_score = scoring_engine.evaluate(var["title"])
            var["score_computed"] = opt_score.overall_score
            var["score_delta"] = round(opt_score.overall_score - original_score.overall_score, 1)
        except Exception:
            var["score_computed"] = var.get("score_estimate", 0)
            var["score_delta"] = 0

    response = {
        "original_title": title,
        "original_score": original_score.overall_score,
        "strategy": strategy,
        "category": category,
        "variations": variations,
        "seeds_used": seeds_used,
    }
    if warnings:
        response["warnings"] = warnings

    # Cache result
    await cache_set(ck, response, ttl=86400)
    return response


def optimize_title_sync(
    title: str,
    strategy: str = "auto",
    category: str | None = None,
    count: int = 4,
) -> dict[str, Any]:
    """Synchronous wrapper for Celery tasks."""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        raise RuntimeError("Cannot call sync function from async context")
    except RuntimeError:
        pass

    return asyncio.run(optimize_title(title, strategy, category, count))
