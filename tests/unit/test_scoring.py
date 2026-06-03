import pytest
from algorithms.scoring import create_scoring_engine
from algorithms.scoring.engine import ScoreResult


@pytest.fixture
def engine():
    return create_scoring_engine()


def test_empty_title(engine):
    with pytest.raises(ValueError, match="标题不能为空"):
        engine.evaluate("")


def test_too_long_title(engine):
    with pytest.raises(ValueError, match="标题长度不能超过200字"):
        engine.evaluate("x" * 201)


def test_valid_title(engine):
    result = engine.evaluate("这绝对是今年最炸裂的干货分享")
    assert isinstance(result, ScoreResult)
    assert 0 <= result.overall_score <= 100
    assert len(result.dimensions) == 4
    dim_names = {d.name for d in result.dimensions}
    assert dim_names == {"attractiveness", "informativeness", "readability", "platform_fit"}


def test_high_attractiveness_title(engine):
    result = engine.evaluate("绝了！99%的人不知道的3个手机摄影技巧 #拍照 #教程")
    attr = next(d for d in result.dimensions if d.name == "attractiveness")
    assert attr.score >= 70


def test_low_attractiveness_title(engine):
    result = engine.evaluate("今天做了红烧肉的做法教程")
    attr = next(d for d in result.dimensions if d.name == "attractiveness")
    assert attr.score < 50


def test_informative_title(engine):
    result = engine.evaluate("3个方法让你7天内涨粉1000")
    info = next(d for d in result.dimensions if d.name == "informativeness")
    assert info.score >= 70


def test_readability_penalty_long(engine):
    result = engine.evaluate("这是一个非常长的标题" + "测试" * 30)
    read = next(d for d in result.dimensions if d.name == "readability")
    assert read.score < 60


def test_platform_fit_with_emoji_tags(engine):
    result = engine.evaluate("绝了！这个方法太好用了 🔥 #教程 #技巧 #干货")
    pf = next(d for d in result.dimensions if d.name == "platform_fit")
    assert pf.score >= 70


def test_platform_fit_no_tags(engine):
    result = engine.evaluate("一个普通标题")
    pf = next(d for d in result.dimensions if d.name == "platform_fit")
    assert pf.score < 50


def test_explanations_contain_required_fields(engine):
    result = engine.evaluate("测试标题")
    for dim, exp in result.explanations.items():
        assert "diagnosis" in exp
        assert "improvement" in exp
        assert "expected_effect" in exp
