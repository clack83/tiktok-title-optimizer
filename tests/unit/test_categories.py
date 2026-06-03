import os
import tempfile
import pytest

from algorithms.nlp.category_loader import get_categories, get_category, get_category_ids, get_category_context, force_reload


def test_get_categories():
    categories = get_categories()
    assert len(categories) >= 10
    assert "游戏" in categories
    assert "生活" in categories
    assert "美食" in categories


def test_get_single_category():
    cat = get_category("游戏")
    assert cat is not None
    assert cat["name"] == "游戏"
    assert len(cat["context_keywords"]) > 0
    assert len(cat["hook_patterns"]) >= 3
    assert "audience" in cat
    assert "taboos" in cat


def test_get_nonexistent_category():
    assert get_category("invalid_category") is None


def test_get_category_ids():
    ids = get_category_ids()
    assert "游戏" in ids
    assert len(ids) >= 10


def test_category_context_contains_key_info():
    ctx = get_category_context("美食")
    assert "美食" in ctx
    assert "教程" in ctx or "食谱" in ctx
    assert "hook" in ctx.lower() or "钩子" in ctx


def test_category_context_invalid():
    ctx = get_category_context("invalid")
    assert ctx == ""


def test_all_categories_have_required_fields():
    for cat_id, cat in get_categories().items():
        assert "name" in cat, f"{cat_id} missing name"
        assert "audience" in cat, f"{cat_id} missing audience"
        assert "context_keywords" in cat, f"{cat_id} missing context_keywords"
        assert "hook_patterns" in cat, f"{cat_id} missing hook_patterns"
        assert len(cat["hook_patterns"]) >= 3, f"{cat_id} needs >=3 hook_patterns"
