from algorithms.nlp.keyword_extractor import extract_keywords
from algorithms.nlp.topic_matcher import match_topics, SEED_TOPICS


def test_extract_keywords_basic():
    result = extract_keywords("新手必看的5个手机摄影技巧")
    assert len(result) > 0
    keywords = [k["keyword"] for k in result]
    assert any("手机摄影" in kw or "摄影" in kw for kw in keywords) or any("新手" in kw for kw in keywords)


def test_extract_keywords_with_weights():
    result = extract_keywords("抖音标题优化工具帮助你提升播放量")
    assert len(result) > 0
    for k in result:
        assert "keyword" in k
        assert "weight" in k
        assert 0 <= k["weight"] <= 1


def test_extract_keywords_empty():
    result = extract_keywords("")
    assert result == []


def test_match_topics_found():
    keywords = [{"keyword": "手机摄影", "weight": 0.5}, {"keyword": "技巧", "weight": 0.3}]
    matches = match_topics(keywords)
    assert len(matches) > 0
    assert any(m["topic"] == "手机摄影" for m in matches)


def test_match_topics_not_found():
    keywords = [{"keyword": "xyzabc", "weight": 0.5}]
    matches = match_topics(keywords)
    assert matches == []


def test_seed_topics_have_required_fields():
    for topic in SEED_TOPICS:
        assert "topic" in topic
        assert "category" in topic
        assert "trend_score" in topic
        assert "level" in topic
        assert "hashtags" in topic
