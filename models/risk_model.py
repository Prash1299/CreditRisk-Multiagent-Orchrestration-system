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
        return cls(None)

    def save(self) -> None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, MODEL_PATH)

    def predict(self, features: dict) -> RiskPrediction:
        row = [
            [
                float(features.get("credit_score", 0)),
                float(features.get("foir", 0)),
                float(features.get("loan_to_income", 0)),
                float(features.get("defaults", 0)),
            ]
        ]
        pd = _heuristic_pd(features)
        if self.pipeline is not None:
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


def _heuristic_pd(features: dict) -> float:
    credit = float(features.get("credit_score", 650) or 650)
    foir = float(features.get("foir", 0.4) or 0.4)
    lti = float(features.get("loan_to_income", 0.5) or 0.5)
    defaults = float(features.get("defaults", 0) or 0)
    raw = (
        0.40 * (1 - min(credit, 850) / 850)
        + 0.30 * foir
        + 0.20 * min(lti, 1.5) / 1.5
        + 0.10 * min(defaults, 3)
    )
    return max(0.02, min(raw, 0.92))
