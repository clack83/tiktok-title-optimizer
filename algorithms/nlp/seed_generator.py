import logging
from typing import Any

import jieba

from algorithms.optimizer.deepseek_client import deepseek_client
from algorithms.scoring import create_scoring_engine
from algorithms.nlp.category_loader import get_category, get_category_context

logger = logging.getLogger(__name__)

scoring_engine = create_scoring_engine()

SEED_GENERATION_PROMPT = """你是一名抖音爆款标题专家。请为"{category_name}"领域生成{candidate_count}条高质量的抖音爆款标题。

{category_context}

要求：
1. 每条标题必须符合该领域的爆款特征
2. 使用不同的钩子类型：疑问式、数字列表式、争议式、情感故事式、认知缺口式
3. 避免生成风格相似的标题，确保多样性
4. 标题长度控制在30-80字
5. 包含中文、emoji和标签

请严格按照以下JSON格式输出：
{{
  "titles": [
    {{"title": "爆款标题1", "hook_type": "question"}},
    {{"title": "爆款标题2", "hook_type": "number_list"}},
    ...
  ]
}}"""


def _tokenize(text: str) -> set[str]:
    return set(jieba.lcut(text))


def _token_overlap(title1: str, title2: str) -> float:
    tokens1 = _tokenize(title1)
    tokens2 = _tokenize(title2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    return len(intersection) / len(union)


def generate_seeds(category: str, candidate_count: int = 25, target_count: int = 20) -> list[dict[str, Any]]:
    cat = get_category(category)
    if not cat:
        raise ValueError(f"分类 '{category}' 不存在")

    all_seeds: list[dict[str, Any]] = []
    hook_types_seen: set[str] = set()
    round_count = 0
    max_rounds = 3

    while len(all_seeds) < target_count and round_count < max_rounds:
        round_count += 1
        if round_count > 1:
            logger.info(f"Seed generation round {round_count} for category '{category}', need more candidates")

        try:
            result = deepseek_client.chat_completion(
                SEED_GENERATION_PROMPT.format(
                    category_name=cat["name"],
                    candidate_count=candidate_count + 10 * (round_count - 1),
                    category_context=get_category_context(category),
                ),
                "请生成标题列表",
                temperature=0.9,
            )
        except Exception as e:
            logger.error(f"DeepSeek seed generation failed for '{category}': {e}")
            raise

        titles_raw = result.get("titles", [])
        for item in titles_raw:
            title = item.get("title", "").strip()
            hook_type = item.get("hook_type", "general")
            if not title:
                continue

            try:
                score_result = scoring_engine.evaluate(title)
                score = int(score_result.overall_score)
            except Exception:
                score = 50

            if score < 70:
                continue

            # Dedup check
            is_dup = False
            for seed in all_seeds:
                if _token_overlap(title, seed["title"]) > 0.8:
                    if score > seed["score"]:
                        seed["title"] = title
                        seed["score"] = score
                        seed["hook_type"] = hook_type
                    is_dup = True
                    break
            if is_dup:
                continue

            all_seeds.append({
                "title": title,
                "score": score,
                "hook_type": hook_type,
            })
            hook_types_seen.add(hook_type)

        logger.info(f"Round {round_count}: {len(titles_raw)} candidates → {len(all_seeds)} qualified seeds")

    # Sort by score desc
    all_seeds.sort(key=lambda s: s["score"], reverse=True)

    logger.info(f"Seed generation for '{category}' complete: {len(all_seeds)} seeds ({len(hook_types_seen)} hook types)")
    return all_seeds[:target_count]


def select_fewshot_seeds(user_title: str, category: str, seeds: list[dict], top_n: int = 5) -> list[dict]:
    """Select top-N seeds based on keyword overlap with user title."""
    if not seeds:
        return []

    user_tokens = _tokenize(user_title)
    if not user_tokens:
        return seeds[:top_n]

    scored = []
    for seed in seeds:
        overlap = len(user_tokens & _tokenize(seed["title"]))
        scored.append((overlap, seed))

    scored.sort(key=lambda x: x[0], reverse=True)
    if scored[0][0] >= 2:
        return [s for _, s in scored[:top_n]]
    return seeds[:top_n]
