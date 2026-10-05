"""Shared CSV, project-path, and benchmark helpers."""

from __future__ import annotations

from pathlib import Path
from typing import IO

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'Customer_churn.csv'
ROC_PLOT_PATH = PROJECT_ROOT / 'reports' / '06_roc_curves_all_models.png'


def read_customer_csv(source: str | Path | IO[bytes] | IO[str]) -> pd.DataFrame:
    """Read and minimally validate customer data from a CSV source.

    Args:
        source: File path or file-like object accepted by ``pandas.read_csv``.

    Returns:
        A non-empty customer DataFrame.

    Raises:
        ValueError: If the CSV has no records or duplicate column names.
    """
    data = pd.read_csv(source)
    if data.empty:
        raise ValueError('The CSV contains no customer rows.')
    if data.columns.has_duplicates:
        raise ValueError('The CSV contains duplicate column names.')
    return data


def load_reference_data() -> pd.DataFrame:
    """Load the project's original churn dataset for dashboard context."""
    return read_customer_csv(REFERENCE_DATA_PATH)


def load_model_benchmarks() -> pd.DataFrame:
    """Return held-out and CV ROC AUC scores reported by the evaluation notebook.

    Baseline values are from the fixed stratified test split. The tuned model
    uses the best training-only randomized-search CV score and the same held-out
    test set; it remains below the project's 0.85 test-AUC goal.
    """
    return pd.DataFrame([
        {'Model': 'Gradient Boosting', 'CV ROC AUC': 0.8490, 'Test ROC AUC': 0.8428},
        {'Model': 'Logistic Regression', 'CV ROC AUC': 0.8464, 'Test ROC AUC': 0.8416},
        {'Model': 'Random Forest', 'CV ROC AUC': 0.8249, 'Test ROC AUC': 0.8240},
        {'Model': 'Extra Trees', 'CV ROC AUC': 0.7944, 'Test ROC AUC': 0.7954},
        {'Model': 'Decision Tree', 'CV ROC AUC': 0.6537, 'Test ROC AUC': 0.6296},
        {'Model': 'Tuned Gradient Boosting', 'CV ROC AUC': 0.8509, 'Test ROC AUC': 0.8476},
    ])