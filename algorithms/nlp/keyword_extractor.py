import os
from collections import Counter
from typing import Any

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

CUSTOM_DICT = os.path.join(os.path.dirname(__file__), "douyin_dict.txt")

# Load custom dictionary if exists
if os.path.exists(CUSTOM_DICT):
    jieba.load_userdict(CUSTOM_DICT)

# Default TikTok-specific terms
TIKTOK_TERMS = [
    "yyds", "破防了", "我悟了", "内卷", "躺平", "绝绝子", "栓Q",
    "天花板", "遥遥领先", "遥遥邻先", "芭比Q", "显眼包", "特种兵旅游",
    "多巴胺穿搭", "美拉德", "city不city", "电子榨菜",
]
for term in TIKTOK_TERMS:
    jieba.add_word(term)


def extract_keywords(title: str, top_n: int = 10) -> list[dict[str, Any]]:
    words = jieba.lcut(title)
    words = [w.strip() for w in words if len(w.strip()) >= 2 and not w.isspace()]

    if not words:
        return []

    try:
        vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
        tfidf_matrix = vectorizer.fit_transform([words])
    except ValueError:
        # Single word case, fallback to frequency
        counter = Counter(words)
        total = sum(counter.values())
        return [
            {"keyword": w, "weight": round(c / total, 3)}
            for w, c in counter.most_common(top_n)
        ]

    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    scored = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)
    return [{"keyword": w, "weight": round(s, 4)} for w, s in scored[:top_n]]
