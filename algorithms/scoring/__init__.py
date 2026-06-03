from algorithms.scoring.engine import ScoringEngine, ScoreResult, DimensionScore
from algorithms.scoring.rules import create_default_rules


def create_scoring_engine() -> ScoringEngine:
    engine = ScoringEngine()
    for rule in create_default_rules():
        engine.register(rule)
    return engine
