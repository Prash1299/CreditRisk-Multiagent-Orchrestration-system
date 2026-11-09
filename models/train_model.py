import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from models.risk_model import RiskModel


def train(seed: int = 42) -> RiskModel:
    rng = np.random.default_rng(seed)
    n = 400
    credit = rng.integers(520, 820, size=n)
    dti = rng.uniform(0.1, 0.7, size=n)
    ltv = rng.uniform(0.3, 1.1, size=n)
    defaults = rng.integers(0, 3, size=n)
    x = np.column_stack([credit, dti, ltv, defaults])
    risk = (
        0.004 * (750 - credit)
        + 1.8 * dti
        + 1.2 * ltv
        + 0.6 * defaults
        + rng.normal(0, 0.3, size=n)
    )
    y = (risk > 1.6).astype(int)

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=400)),
        ]
    )
    pipeline.fit(x, y)
    model = RiskModel(pipeline)
    model.save()
    return model


if __name__ == "__main__":
    train()
    print("Saved model to data/risk_model.joblib")
