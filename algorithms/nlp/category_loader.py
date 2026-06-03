import os
import threading
import time
import logging
from typing import Any

import yaml

logger = logging.getLogger(__name__)

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "..", "categories.yaml")

_categories: dict[str, Any] = {}
_last_loaded: float = 0
_reload_interval: float = 60.0
_lock = threading.Lock()


def _load_yaml() -> dict[str, Any]:
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("categories", {})


def get_categories() -> dict[str, Any]:
    global _categories, _last_loaded

    now = time.time()
    with _lock:
        if now - _last_loaded > _reload_interval:
            try:
                _categories = _load_yaml()
                _last_loaded = now
                logger.info(f"Reloaded categories config ({len(_categories)} categories)")
            except Exception as e:
                logger.error(f"Failed to reload categories: {e}")
                if not _categories:
                    raise

    return _categories


def get_category(category_id: str) -> dict[str, Any] | None:
    categories = get_categories()
    return categories.get(category_id)


def get_category_ids() -> list[str]:
    return list(get_categories().keys())


def get_category_context(category_id: str) -> str:
    """Build category-specific context for prompt injection."""
    cat = get_category(category_id)
    if not cat:
        return ""

    parts = [
        f"内容领域：{cat['name']}",
        f"目标受众：{cat['audience']}",
        f"领域关键词：{', '.join(cat['context_keywords'])}",
        f"爆款钩子模板：{'; '.join(cat['hook_patterns'][:3])}",
    ]

    if cat.get("taboos"):
        parts.append(f"禁止：{'；'.join(cat['taboos'])}")

    return "\n".join(parts)


def force_reload():
    """Force immediate reload of categories config."""
    global _categories, _last_loaded
    with _lock:
        try:
            _categories = _load_yaml()
            _last_loaded = time.time()
        except Exception as e:
            logger.error(f"Failed to force reload categories: {e}")
