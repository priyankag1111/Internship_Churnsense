"""Loading and scoring the serialized churn-prediction pipeline."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.preprocessing import prepare_features

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = PROJECT_ROOT / 'models' / 'churn_model_v1.pkl'


def load_model(model_path: str | Path = DEFAULT_MODEL_PATH):
    """Load a fitted model pipeline that supports churn probabilities.

    Args:
        model_path: Path to a joblib-serialized fitted sklearn pipeline.

    Returns:
        The loaded fitted pipeline.

    Raises:
        FileNotFoundError: If the model artifact does not exist.
        TypeError: If the artifact does not expose ``predict_proba``.
    """
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(f'Model artifact not found: {path}')
    model = joblib.load(path)
    if not callable(getattr(model, 'predict_proba', None)):
        raise TypeError(f'Model artifact does not support predict_proba: {path}')
    return model


def predict_customers(
    data: pd.DataFrame,
    model=None,
    threshold: float = 0.5,
) -> pd.DataFrame:
    """Score customer rows and append churn probability and risk labels.

    Args:
        data: Raw customer rows; may include ``customerID`` and/or ``Churn``.
        model: Optional fitted pipeline. The saved project model is loaded when
            this argument is omitted.
        threshold: Probability cutoff used for the binary churn prediction.

    Returns:
        A copy of the input without its target label, plus predicted churn,
        churn probability, and a three-level risk band.

    Raises:
        ValueError: If the threshold is outside [0, 1].
    """
    if not 0 <= threshold <= 1:
        raise ValueError('threshold must be between 0 and 1 inclusive.')

    predictor = model if model is not None else load_model()
    features = prepare_features(data)
    probabilities = predictor.predict_proba(features)[:, 1]
    scored = data.drop(columns=['Churn'], errors='ignore').copy()
    scored['churn_probability'] = probabilities
    scored['predicted_churn'] = np.where(probabilities >= threshold, 'Churn', 'No churn')
    scored['risk_level'] = pd.cut(
        probabilities,
        bins=[-np.inf, 0.30, 0.60, np.inf],
        labels=['Low', 'Medium', 'High'],
        right=False,
    ).astype(str)
    return scored