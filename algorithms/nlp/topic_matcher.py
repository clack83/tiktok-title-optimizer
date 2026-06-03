from typing import Any

# Seed trending topics (extensible)
SEED_TOPICS = [
    {"topic": "手机摄影", "category": "科技", "trend_score": 85, "level": "high",
     "hashtags": ["#手机摄影", "#拍照技巧", "#手机拍大片"]},
    {"topic": "新手化妆", "category": "美妆", "trend_score": 78, "level": "high",
     "hashtags": ["#新手化妆", "#化妆教程", "#美妆技巧"]},
    {"topic": "王者荣耀", "category": "游戏", "trend_score": 92, "level": "high",
     "hashtags": ["#王者荣耀", "#游戏攻略", "#上分"]},
    {"topic": "减肥", "category": "健身", "trend_score": 80, "level": "high",
     "hashtags": ["#减肥", "#瘦身", "#健身"]},
    {"topic": "美食教程", "category": "美食", "trend_score": 75, "level": "medium",
     "hashtags": ["#美食教程", "#家常菜", "#做饭"]},
    {"topic": "旅行攻略", "category": "旅行", "trend_score": 82, "level": "high",
     "hashtags": ["#旅行攻略", "#旅游", "#打卡"]},
    {"topic": "职场", "category": "职场", "trend_score": 70, "level": "medium",
     "hashtags": ["#职场", "#打工人", "#工资"]},
    {"topic": "情感", "category": "婚恋", "trend_score": 76, "level": "high",
     "hashtags": ["#情感", "#恋爱", "#婚姻"]},
    {"topic": "教育", "category": "教育", "trend_score": 68, "level": "medium",
     "hashtags": ["#教育", "#学习", "#考试"]},
    {"topic": "生活妙招", "category": "生活", "trend_score": 73, "level": "medium",
     "hashtags": ["#生活妙招", "#实用技巧", "#居家"]},
]


def match_topics(keywords: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matches = []
    keyword_text = " ".join(k["keyword"] for k in keywords)

    for topic in SEED_TOPICS:
        if topic["topic"] in keyword_text or any(
            k["keyword"] in topic["topic"] or topic["topic"] in k["keyword"]
            for k in keywords
        ):
            matches.append(topic)

    if not matches:
        return []

    matches.sort(key=lambda t: t["trend_score"], reverse=True)
    return matches
