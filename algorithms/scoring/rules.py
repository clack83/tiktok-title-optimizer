import re
from algorithms.scoring.engine import ScoringRule


# ============================================================
# Helpers
# ============================================================

POWER_WORDS = [
    "绝了", "万万没想到", "99%的人不知道", "后悔没早", "这才是真正的",
    "建议收藏", "史上最", "一招搞定", "秒变", "逆袭", "炸裂", "封神",
    "天花板", "永远可以相信", "教科书级", "我悟了",
]

EMOTIONAL_WORDS = [
    "哭了", "破防", "笑死", "离谱", "不敢相信", "太真实了",
    "谁能想到", "彻底服了", "这才是", "终于",
]

CURIOSITY_HOOKS = [
    "为什么", "到底", "竟然", "原来", "真相是", "揭秘", "曝光",
    "背后的秘密", "你可能不知道", "别再",
]

EMOJI_PATTERN = re.compile(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2764\uFE0F\u200D]')
HASHTAG_PATTERN = re.compile(r'#[\w\u4e00-\u9fff]+')
NUMBER_PATTERN = re.compile(r'\d+')


def _clamp(v: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, v))


def _has_numbers(title: str) -> bool:
    return bool(NUMBER_PATTERN.search(title))


def _count_emojis(title: str) -> int:
    return len(EMOJI_PATTERN.findall(title))


def _count_hashtags(title: str) -> int:
    return len(HASHTAG_PATTERN.findall(title))


def _count_power_words(title: str) -> int:
    return sum(1 for w in POWER_WORDS if w in title)


def _count_emotional_words(title: str) -> int:
    return sum(1 for w in EMOTIONAL_WORDS if w in title)


def _count_curiosity_hooks(title: str) -> int:
    return sum(1 for h in CURIOSITY_HOOKS if h in title)


# ============================================================
# Dimension: Attractiveness (weight: 0.40)
# ============================================================

def _eval_attractiveness(title: str) -> float:
    score = 30.0
    score += min(20, _count_power_words(title) * 10)
    score += min(15, _count_emotional_words(title) * 7.5)
    score += min(15, _count_curiosity_hooks(title) * 7.5)
    score += 10 if _has_numbers(title) else 0
    score += 10 if len(title) <= 40 else (5 if len(title) <= 60 else 0)
    return _clamp(score)


def _explain_attractiveness(title: str, score: float) -> dict:
    pw = _count_power_words(title)
    emo = _count_emotional_words(title)
    cur = _count_curiosity_hooks(title)

    if score >= 70:
        diag = f"标题吸引力强，包含{['零',''][pw] if pw else ''}个权力词、{'情绪触发词和' if emo else ''}好奇心钩子，能有效驱动点击"
        imp = "继续保持hook节奏，可尝试加入更多争议性或反常识表达"
        eff = "可维持高点击率"
    elif score >= 50:
        missing = []
        if pw == 0:
            missing.append("权力词（如'绝了''封神'）")
        if emo == 0:
            missing.append("情绪触发词")
        if cur == 0:
            missing.append("好奇心钩子")
        diag = f"标题吸引力一般，缺少{', '.join(missing) if missing else '冲击力表达'}"
        imp = f"建议在开头8个字内加入{missing[0] if missing else '情绪词或数字'}"
        eff = "预计吸引力提升15-25分"
    else:
        diag = "标题缺乏hook，读者没有点击欲望，需要大幅增强开头吸引力"
        imp = "在前半句加入数字+反常识组合，例如'3个方法...'或'90%的人不知道...'"
        eff = "预计吸引力提升25-40分"

    return {"diagnosis": diag, "improvement": imp, "expected_effect": eff}


# ============================================================
# Dimension: Informativeness (weight: 0.25)
# ============================================================

def _eval_informativeness(title: str) -> float:
    score = 20.0
    score += 20 if _has_numbers(title) else 0
    score += min(25, len(title) / 2.4)
    score += 15 if any(kw in title for kw in ["教程", "方法", "步骤", "攻略", "技巧", "指南", "干货"]) else 0
    score += 10 if len(title) >= 15 else 0
    return _clamp(score)


def _explain_informativeness(title: str, score: float) -> dict:
    has_num = _has_numbers(title)
    has_kw = any(kw in title for kw in ["教程", "方法", "步骤", "攻略", "技巧", "指南", "干货"])

    if score >= 70:
        diag = "信息密度高，明确给出了内容承诺和具体信息点"
        imp = "保持结构化表达，可适当加入具体数字增强可信度"
        eff = "信息量充足，用户预期明确"
    else:
        parts = []
        if not has_num:
            parts.append("缺少具体数字")
        if not has_kw:
            parts.append("缺少内容类型词（教程/攻略/方法）")
        diag = f"信息量偏低：{'；'.join(parts)}"
        imp = "加入具体数字和内容类型承诺，如'3个技巧'、'保姆级教程'"
        eff = "预计信息量提升15-20分"

    return {"diagnosis": diag, "improvement": imp, "expected_effect": eff}


# ============================================================
# Dimension: Readability (weight: 0.20)
# ============================================================

def _eval_readability(title: str) -> float:
    score = 60.0
    if len(title) > 80:
        score -= min(30, (len(title) - 80) * 0.8)
    if len(title) < 8:
        score -= 20
    if re.search(r'[，,、\s]', title):
        score += 10
    if len(title) <= 50:
        score += 10
    return _clamp(score)


def _explain_readability(title: str, score: float) -> dict:
    if score >= 70:
        diag = "标题长度适中，结构清晰，易于快速阅读"
        imp = "保持当前节奏"
        eff = "可读性良好，完播率有保障"
    elif len(title) > 80:
        diag = f"标题过长（{len(title)}字），用户注意力在前3秒会流失"
        imp = f"建议精简至60字以内，删除冗余修饰词"
        eff = "缩短后可读性提升15-25分，完播率上升"
    else:
        diag = "标题偏短，可能信息传达不够完整"
        imp = "适当扩充至15-30字，增加信息但不失简洁"
        eff = "预计可读性提升10-15分"

    return {"diagnosis": diag, "improvement": imp, "expected_effect": eff}


# ============================================================
# Dimension: Platform Fit (weight: 0.15)
# ============================================================

def _eval_platform_fit(title: str) -> float:
    score = 30.0
    emoji_count = _count_emojis(title)
    hash_count = _count_hashtags(title)

    if 1 <= emoji_count <= 3:
        score += 25
    elif emoji_count > 3:
        score += 10

    if 2 <= hash_count <= 5:
        score += 25
    elif hash_count == 1:
        score += 15
    elif hash_count == 0:
        score += 0

    score += 10 if len(title) <= 55 else 0
    return _clamp(score)


def _explain_platform_fit(title: str, score: float) -> dict:
    emoji_count = _count_emojis(title)
    hash_count = _count_hashtags(title)

    if score >= 70:
        diag = "平台适配良好，emoji和标签使用符合抖音最佳实践"
        imp = "微调标签可选择更精准的长尾标签"
        eff = "算法推荐匹配度高"
    else:
        issues = []
        if emoji_count == 0:
            issues.append("未使用emoji")
        elif emoji_count > 3:
            issues.append("emoji过多显得杂乱")
        if hash_count == 0:
            issues.append("缺少标签将降低算法推荐")
        elif hash_count > 5:
            issues.append("标签过多分散权重")
        diag = f"平台适配不足：{'；'.join(issues)}"
        imp = "添加1-3个相关emoji和2-5个精准标签"
        eff = "预计平台适配提升20-35分，增加推荐概率"

    return {"diagnosis": diag, "improvement": imp, "expected_effect": eff}


# ============================================================
# Factory
# ============================================================

def create_default_rules() -> list[ScoringRule]:
    return [
        ScoringRule("attractiveness", 0.40, _eval_attractiveness, _explain_attractiveness),
        ScoringRule("informativeness", 0.25, _eval_informativeness, _explain_informativeness),
        ScoringRule("readability", 0.20, _eval_readability, _explain_readability),
        ScoringRule("platform_fit", 0.15, _eval_platform_fit, _explain_platform_fit),
    ]
