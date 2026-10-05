"""Shared cached resources and page headings for the Streamlit app."""

from __future__ import annotations

import streamlit as st

from src.model import load_model
from src.utils import PROJECT_ROOT, load_reference_data, load_model_benchmarks

SAMPLE_CSV_PATH = PROJECT_ROOT / 'tests' / 'fixtures' / 'new_customers.csv'


@st.cache_resource(show_spinner='Loading churn model...')
def get_model():
    """Load and cache the fitted prediction pipeline for this app process."""
    return load_model()


@st.cache_data(show_spinner=False)
def get_reference_data():
    """Load and cache the historical cohort used by the dashboard."""
    return load_reference_data()


@st.cache_data(show_spinner=False)
def get_benchmarks():
    """Load the model-comparison metrics documented by the evaluation notebook."""
    return load_model_benchmarks()


def page_header(section: str, title: str, subtitle: str) -> None:
    """Render a consistent compact heading for a Streamlit page."""
    st.caption(section.upper())
    st.title(title)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)