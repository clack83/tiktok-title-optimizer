import pytest
from unittest.mock import patch, MagicMock

from algorithms.optimizer.strategies import STRATEGY_PROMPTS, OPTIMIZATION_SYSTEM_PROMPT


def test_strategies_defined():
    expected = {"hook_enhancement", "emotional_amplification", "keyword_optimization", "formatting_polish", "auto"}
    assert set(STRATEGY_PROMPTS.keys()) == expected


def test_auto_strategy_exists():
    assert "auto" in STRATEGY_PROMPTS
    assert "综合优化" in STRATEGY_PROMPTS["auto"]


def test_hook_enhancement_strategy():
    assert "钩子增强" in STRATEGY_PROMPTS["hook_enhancement"]
    assert "前8个字" in STRATEGY_PROMPTS["hook_enhancement"]


def test_system_prompt_format():
    prompt = OPTIMIZATION_SYSTEM_PROMPT.format(
        strategy_instruction="test strategy",
        category_context="",
    )
    assert "test strategy" in prompt
    assert "JSON" in prompt
    assert "change_reasons" in prompt
    assert "variations" in prompt


@patch("algorithms.optimizer.pipeline.cache_get", return_value=None)
@patch("algorithms.optimizer.pipeline.cache_set", return_value=None)
@patch("algorithms.optimizer.pipeline.deepseek_client")
def test_optimize_pipeline_basic(mock_client, mock_cache_set, mock_cache_get):
    mock_client.chat_completion.return_value = {
        "variations": [
            {
                "title": "优化后的标题测试",
                "score_estimate": 85,
                "change_reasons": [
                    {
                        "category": "hook_enhancement",
                        "comparison": {"before": "原标题", "after": "新标题"},
                        "reason": "增强了吸引力",
                        "expected_effect": "提升点击率",
                    }
                ],
            }
        ]
    }

    from algorithms.optimizer.pipeline import optimize_title_sync
    result = optimize_title_sync("测试标题", "auto", None)

    assert result["original_title"] == "测试标题"
    assert len(result["variations"]) == 1
    assert result["variations"][0]["title"] == "优化后的标题测试"
    assert "score_computed" in result["variations"][0]


def test_optimize_empty_title():
    import asyncio
    from algorithms.optimizer.pipeline import optimize_title

    async def run():
        with pytest.raises(ValueError, match="标题不能为空"):
            await optimize_title("")

    asyncio.run(run())


def test_reference_seeds_section_format():
    """Test that REFERENCE_SEEDS_SECTION contains proper template variable."""
    from algorithms.optimizer.strategies import REFERENCE_SEEDS_SECTION
    assert "{seed_titles}" in REFERENCE_SEEDS_SECTION
    formatted = REFERENCE_SEEDS_SECTION.format(seed_titles="- [question] 测试标题 (评分: 85)")
    assert "测试标题" in formatted
    assert "评分: 85" in formatted


def test_user_prompt_has_reference_seeds_token():
    """Test that OPTIMIZATION_USER_PROMPT has the reference_seeds placeholder."""
    from algorithms.optimizer.strategies import OPTIMIZATION_USER_PROMPT
    assert "{reference_seeds}" in OPTIMIZATION_USER_PROMPT


def test_user_prompt_format_with_seeds():
    """Test formatting the user prompt with reference seeds included."""
    from algorithms.optimizer.strategies import OPTIMIZATION_USER_PROMPT, REFERENCE_SEEDS_SECTION

    seed_section = REFERENCE_SEEDS_SECTION.format(
        seed_titles="- [question] 爆款参考标题 (评分: 88)\n- [number_list] 另一个参考标题 (评分: 82)"
    )
    prompt = OPTIMIZATION_USER_PROMPT.format(
        original_title="测试原标题",
        reference_seeds=seed_section,
        count=4,
    )
    assert "测试原标题" in prompt
    assert "爆款参考标题" in prompt
    assert "4" in prompt


def test_user_prompt_format_without_seeds():
    """Test formatting the user prompt without reference seeds (degrade)."""
    from algorithms.optimizer.strategies import OPTIMIZATION_USER_PROMPT

    prompt = OPTIMIZATION_USER_PROMPT.format(
        original_title="测试原标题",
        reference_seeds="",
        count=3,
    )
    assert "测试原标题" in prompt
    assert "3" in prompt
    # Should still work without seeds section
    assert "请优化这个标题" in prompt


@patch("algorithms.optimizer.pipeline.cache_get", return_value=None)
@patch("algorithms.optimizer.pipeline.cache_set", return_value=None)
@patch("algorithms.optimizer.pipeline.deepseek_client")
def test_optimize_pipeline_without_seeds_no_category(mock_client, mock_cache_set, mock_cache_get):
    """Test optimization without category produces no seeds_used."""
    mock_client.chat_completion.return_value = {
        "variations": [
            {
                "title": "优化后标题",
                "score_estimate": 80,
                "change_reasons": [],
            }
        ]
    }

    from algorithms.optimizer.pipeline import optimize_title_sync
    result = optimize_title_sync("测试标题", "auto", None)

    assert result["seeds_used"] == []
    assert "warnings" not in result
