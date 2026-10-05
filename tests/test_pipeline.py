"""Tests for customer churn preprocessing and prediction workflows."""

from pathlib import Path

import pandas as pd
import pytest

from src.model import predict_customers
from src.preprocessing import prepare_features
from src.utils import read_customer_csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NEW_CUSTOMERS_PATH = Path(__file__).parent / 'fixtures' / 'new_customers.csv'


def test_feature_builder_matches_model_contract() -> None:
    """Create the two engineered features and omit ID/target from model input."""
    customers = read_customer_csv(NEW_CUSTOMERS_PATH)

    features = prepare_features(customers)

    assert 'customerID' not in features.columns
    assert 'Churn' not in features.columns
    assert features.loc[0, 'tenure_monthly_charge_ratio'] == 0
    assert features.loc[0, 'long_term_customer'] == 0
    assert features.loc[1, 'long_term_customer'] == 1
    assert features['TotalCharges'].isna().sum() == 1


def test_new_csv_scores_unknown_categories_and_missing_charges() -> None:
    """Score a separately authored CSV with unseen categories and blank charges."""
    customers = read_customer_csv(NEW_CUSTOMERS_PATH)

    scored = predict_customers(customers)

    assert len(scored) == 4
    assert scored['customerID'].tolist() == ['NEW-0001', 'NEW-0002', 'NEW-0003', 'NEW-0004']
    assert scored['churn_probability'].between(0, 1).all()
    assert scored['predicted_churn'].isin(['Churn', 'No churn']).all()
    assert scored['risk_level'].isin(['Low', 'Medium', 'High']).all()
    assert scored['source_note'].eq('synthetic prospect').all()


def test_missing_required_feature_has_actionable_error() -> None:
    """Reject an incomplete upload with the missing feature named."""
    customers = read_customer_csv(NEW_CUSTOMERS_PATH).drop(columns=['Contract'])

    with pytest.raises(ValueError, match='Contract'):
        prepare_features(customers)


def test_invalid_threshold_is_rejected() -> None:
    """Keep the classification threshold within its probability domain."""
    customers = read_customer_csv(NEW_CUSTOMERS_PATH)

    with pytest.raises(ValueError, match='between 0 and 1'):
        predict_customers(customers, threshold=1.1)


def test_empty_csv_is_rejected() -> None:
    """Reject a CSV with a header but no customer records."""
    empty_csv = pd.io.common.StringIO('gender,tenure\n')

    with pytest.raises(ValueError, match='no customer rows'):
        read_customer_csv(empty_csv)