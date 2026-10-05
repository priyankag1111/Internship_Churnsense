"""Input validation and feature preparation for churn predictions."""

from __future__ import annotations

import pandas as pd

RAW_FEATURE_COLUMNS = (
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
    'MonthlyCharges', 'TotalCharges',
)

NUMERIC_COLUMNS = ('SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges')


def prepare_features(data: pd.DataFrame) -> pd.DataFrame:
    """Validate raw customer rows and create the exact features used in training.

    Customer identifiers and an optional target column are deliberately excluded
    from model input. Additional columns are ignored so uploaded files may carry
    harmless metadata without changing the fitted model's feature schema.

    Args:
        data: Raw customer records, with one row per customer.

    Returns:
        A DataFrame ordered to match the raw model feature contract, including
        the two deterministic engineered features.

    Raises:
        TypeError: If ``data`` is not a pandas DataFrame.
        ValueError: If the frame is empty, has duplicate columns, or is missing
            any required customer feature.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError('Customer input must be a pandas DataFrame.')
    if data.empty:
        raise ValueError('Customer input contains no rows.')
    if data.columns.has_duplicates:
        raise ValueError('Customer input contains duplicate column names.')

    missing_columns = sorted(set(RAW_FEATURE_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f'Missing required customer columns: {", ".join(missing_columns)}')

    features = data.loc[:, RAW_FEATURE_COLUMNS].copy()
    for column in NUMERIC_COLUMNS:
        features[column] = pd.to_numeric(features[column], errors='coerce')

    features['tenure_monthly_charge_ratio'] = features['tenure'] / (
        features['MonthlyCharges'] + 1e-6
    )
    features['long_term_customer'] = (features['tenure'] >= 12).astype(int)
    return features