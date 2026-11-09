import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from models.risk_model import MODEL_PATH, RiskModel


def train(seed: int = 42) -> RiskModel:
    rng = np.random.default_rng(seed)
    n = 500
    credit = rng.integers(560, 820, size=n)
    foir = rng.uniform(0.15, 0.75, size=n)
    lti = rng.uniform(0.2, 1.4, size=n)
    defaults = rng.integers(0, 3, size=n)
    x = np.column_stack([credit, foir, lti, defaults])
    risk = 0.004 * (740 - credit) + 2.2 * foir + 0.8 * lti + 0.7 * defaults + rng.normal(0, 0.25, n)
    y = (risk > 1.35).astype(int)
    pipeline = Pipeline(
        [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=400))]
    )
    pipeline.fit(x, y)
    model = RiskModel(pipeline)
    model.save()
    return model


if __name__ == "__main__":
    train()
    print(f"Saved model to {MODEL_PATH}")
