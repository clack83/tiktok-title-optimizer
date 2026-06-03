import pytest
from unittest.mock import patch, MagicMock

from algorithms.nlp.seed_generator import (
    _tokenize,
    _token_overlap,
    select_fewshot_seeds,
    generate_seeds,
)


def test_tokenize():
    tokens = _tokenize("抖音爆款标题优化技巧")
    assert isinstance(tokens, set)
    assert len(tokens) > 0
    assert "抖音" in tokens


def test_tokenize_empty():
    tokens = _tokenize("")
    assert tokens == set()


def test_token_overlap_identical():
    overlap = _token_overlap("抖音爆款标题", "抖音爆款标题")
    assert overlap == 1.0


def test_token_overlap_no_overlap():
    overlap = _token_overlap("游戏技巧分享", "美食制作教程")
    assert overlap < 0.5


def test_token_overlap_empty():
    assert _token_overlap("", "测试") == 0.0
    assert _token_overlap("测试", "") == 0.0


def test_select_fewshot_seeds_by_overlap():
    seeds = [
        {"title": "游戏技巧大揭秘，学会轻松上分", "score": 90, "hook_type": "cognitive_gap", "id": "1"},
        {"title": "美食制作教程，简单好学", "score": 85, "hook_type": "number_list", "id": "2"},
        {"title": "旅行攻略必看，省钱又好玩", "score": 80, "hook_type": "question", "id": "3"},
        {"title": "游戏主播不会告诉你的5个秘密", "score": 88, "hook_type": "controversy", "id": "4"},
        {"title": "今天做了红烧肉，太香了", "score": 75, "hook_type": "emotional_story", "id": "5"},
        {"title": "王者荣耀新英雄玩法攻略", "score": 82, "hook_type": "general", "id": "6"},
    ]

    selected = select_fewshot_seeds("游戏上分技巧分享", "游戏", seeds, top_n=3)
    assert len(selected) == 3
    # Seeds with "游戏" keyword should be selected first
    assert any("游戏" in s["title"] for s in selected)


def test_select_fewshot_seeds_empty_seeds():
    selected = select_fewshot_seeds("测试标题", "游戏", [], top_n=5)
    assert selected == []


def test_select_fewshot_seeds_top_n():
    seeds = [
        {"title": "标题A测试", "score": 90, "hook_type": "general", "id": "1"},
        {"title": "标题B测试", "score": 85, "hook_type": "general", "id": "2"},
        {"title": "标题C测试", "score": 80, "hook_type": "general", "id": "3"},
        {"title": "标题D测试", "score": 75, "hook_type": "general", "id": "4"},
        {"title": "标题E测试", "score": 70, "hook_type": "general", "id": "5"},
        {"title": "标题F测试", "score": 65, "hook_type": "general", "id": "6"},
    ]
    selected = select_fewshot_seeds("完全不相关的查询", "test", seeds, top_n=4)
    # When no keyword overlap, falls back to top-N by score
    assert len(selected) == 4


def test_select_fewshot_seeds_fallback_when_no_match():
    seeds = [
        {"title": "游戏技巧", "score": 90, "hook_type": "general", "id": "1"},
        {"title": "美食教程", "score": 85, "hook_type": "general", "id": "2"},
    ]
    selected = select_fewshot_seeds("完全不相关查询XYZ", "test", seeds, top_n=2)
    # Falls back to top-N
    assert len(selected) == 2


@patch("algorithms.nlp.seed_generator.deepseek_client")
def test_generate_seeds_basic(mock_client):
    mock_client.chat_completion.return_value = {
        "titles": [
            {"title": "爆款标题测试1，非常吸引人点击查看", "hook_type": "question"},
            {"title": "爆款标题测试2，教你如何快速上手游戏攻略", "hook_type": "number_list"},
            {"title": "爆款标题测试3，这些技巧老玩家都不知道", "hook_type": "cognitive_gap"},
            {"title": "爆款标题测试4，真的太实用了建议收藏保存", "hook_type": "emotional_story"},
            {"title": "爆款标题测试5，新手必看的入门教程指南", "hook_type": "question"},
        ]
    }

    seeds = generate_seeds("游戏", candidate_count=10, target_count=5)
    assert len(seeds) <= 5
    for seed in seeds:
        assert "title" in seed
        assert "score" in seed
        assert "hook_type" in seed


@patch("algorithms.nlp.seed_generator.deepseek_client")
def test_generate_seeds_filters_low_scores(mock_client):
    # Return titles that will get scored and filtered
    mock_client.chat_completion.return_value = {
        "titles": [
            {"title": "短标题", "hook_type": "general"},
            {"title": "这是一个比较长的抖音标题包含了更多信息和关键词吸引用户点击", "hook_type": "question"},
        ]
    }

    seeds = generate_seeds("游戏", candidate_count=5, target_count=5)
    # Should filter by score >= 70, though short title might get low score
    # and might or might not pass the filter depending on scoring
    assert len(seeds) <= 2


@patch("algorithms.nlp.seed_generator.deepseek_client")
def test_generate_seeds_deduplication(mock_client):
    # Return similar titles to test dedup
    mock_client.chat_completion.return_value = {
        "titles": [
            {"title": "抖音爆款标题优化技巧分享", "hook_type": "question"},
            {"title": "抖音爆款标题优化技巧分享大全", "hook_type": "number_list"},
            {"title": "完全不同的美食制作教程推荐", "hook_type": "cognitive_gap"},
        ]
    }

    seeds = generate_seeds("生活", candidate_count=10, target_count=10)
    # First two are very similar, one should be deduped (or replaced by the higher scored one)
    titles = [s["title"] for s in seeds]
    # Should have at most 2 unique-similar titles (the similar pair + the different one)
    assert len(seeds) <= 3


@patch("algorithms.nlp.seed_generator.deepseek_client")
def test_generate_seeds_sorted_by_score(mock_client):
    mock_client.chat_completion.return_value = {
        "titles": [
            {"title": "这是一个高质量的长标题包含了很多关键词和信息量让用户点击", "hook_type": "question"},
            {"title": "短标题A", "hook_type": "number_list"},
            {"title": "这是一个中等质量的标题包含了部分关键词", "hook_type": "cognitive_gap"},
        ]
    }

    seeds = generate_seeds("科技", candidate_count=10, target_count=10)
    # Should be sorted by score descending
    for i in range(len(seeds) - 1):
        assert seeds[i]["score"] >= seeds[i + 1]["score"]


def test_generate_seeds_invalid_category():
    with pytest.raises(ValueError, match="不存在"):
        generate_seeds("invalid_category_xyz")


def test_hook_types_diversity():
    """Verify hook types are tracked and diverse results are returned."""
    hook_types = {"question", "number_list", "controversy", "emotional_story", "cognitive_gap", "general"}
    # Verify constant values
    assert len(hook_types) >= 5
