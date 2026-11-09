from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = Path(__file__).resolve().parents[1] / "data" / "risk_model.joblib"


@dataclass
class RiskPrediction:
    probability_of_default: float
    risk_band: str


class RiskModel:
    def __init__(self, pipeline: Pipeline | None = None):
        self.pipeline = pipeline

    @classmethod
    def load(cls) -> RiskModel:
        if MODEL_PATH.exists():
            return cls(joblib.load(MODEL_PATH))
        return cls(_untrained_pipeline())

    def save(self) -> None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, MODEL_PATH)

    def predict(self, features: dict) -> RiskPrediction:
        row = [
            [
                float(features.get("credit_score", 0)),
                float(features.get("dti", 0)),
                float(features.get("ltv", 0)),
                float(features.get("defaults", 0)),
            ]
        ]
        if self.pipeline is None:
            pd = _heuristic_pd(features)
        else:
            try:
                pd = float(self.pipeline.predict_proba(row)[0][1])
            except Exception:
                pd = _heuristic_pd(features)
        if pd < 0.08:
            band = "low"
        elif pd < 0.18:
            band = "medium"
        else:
            band = "high"
        return RiskPrediction(probability_of_default=round(pd, 4), risk_band=band)


def _untrained_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=200)),
        ]
    )


def _heuristic_pd(features: dict) -> float:
    credit = float(features.get("credit_score", 650))
    dti = float(features.get("dti", 0.35))
    ltv = float(features.get("ltv", 0.8))
    defaults = float(features.get("defaults", 0))
    raw = 0.35 * (1 - min(credit, 850) / 850) + 0.3 * dti + 0.25 * ltv + 0.1 * min(defaults, 3)
    return max(0.01, min(raw, 0.95))
