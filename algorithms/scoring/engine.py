from dataclasses import dataclass, field
from typing import Callable


@dataclass
class DimensionScore:
    name: str
    score: float
    weight: float
    diagnosis: str
    improvement: str
    expected_effect: str


@dataclass
class ScoreResult:
    overall_score: float
    dimensions: list[DimensionScore]
    explanations: dict[str, dict]

    @property
    def dimension_scores(self) -> dict[str, float]:
        return {d.name: d.score for d in self.dimensions}


class ScoringRule:
    def __init__(self, dimension: str, weight: float, evaluate_fn: Callable, explain_fn: Callable):
        self.dimension = dimension
        self.weight = weight
        self.evaluate_fn = evaluate_fn
        self.explain_fn = explain_fn

    def evaluate(self, title: str) -> tuple[float, dict]:
        score = self.evaluate_fn(title)
        explanation = self.explain_fn(title, score)
        return score, explanation


class ScoringEngine:
    def __init__(self):
        self.rules: list[ScoringRule] = []

    def register(self, rule: ScoringRule):
        self.rules.append(rule)

    def evaluate(self, title: str) -> ScoreResult:
        if not title.strip():
            raise ValueError("标题不能为空")
        if len(title) > 200:
            raise ValueError("标题长度不能超过200字")

        dimensions = []
        overall = 0.0

        for rule in self.rules:
            score, explanation = rule.evaluate(title)
            weighted = score * rule.weight
            overall += weighted
            dimensions.append(DimensionScore(
                name=rule.dimension,
                score=round(score, 1),
                weight=rule.weight,
                diagnosis=explanation.get("diagnosis", ""),
                improvement=explanation.get("improvement", ""),
                expected_effect=explanation.get("expected_effect", ""),
            ))

        overall = round(overall, 1)

        explanations = {}
        for d in dimensions:
            explanations[d.name] = {
                "score": d.score,
                "diagnosis": d.diagnosis,
                "improvement": d.improvement,
                "expected_effect": d.expected_effect,
            }

        return ScoreResult(
            overall_score=overall,
            dimensions=dimensions,
            explanations=explanations,
        )
