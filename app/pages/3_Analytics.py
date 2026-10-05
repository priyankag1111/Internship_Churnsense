"""Model performance and explainability page."""

import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from app.shared import get_benchmarks, page_header
from src.utils import PROJECT_ROOT, ROC_PLOT_PATH

page_header('Model oversight', 'Model analytics', 'Evaluation · comparison · explainability')

benchmarks = get_benchmarks()
tuned_metrics = benchmarks.loc[benchmarks['Model'] == 'Tuned Gradient Boosting'].iloc[0]
metric_cols = st.columns(3)
metric_cols[0].metric('Held-out test ROC AUC', f"{tuned_metrics['Test ROC AUC']:.4f}")
metric_cols[1].metric('Training CV ROC AUC', f"{tuned_metrics['CV ROC AUC']:.4f}")
metric_cols[2].metric('Test AUC goal', '> 0.8500', delta='Not met', delta_color='inverse')

st.subheader('Candidate comparison')
bar_positions = np.arange(len(benchmarks))
bar_height = 0.36
figure, axis = plt.subplots(figsize=(13, 6), facecolor='#1c2927')
axis.set_facecolor('#1c2927')
axis.barh(
    bar_positions - bar_height / 2,
    benchmarks['CV ROC AUC'],
    height=bar_height,
    color='#087e73',
    label='CV ROC AUC',
)
axis.barh(
    bar_positions + bar_height / 2,
    benchmarks['Test ROC AUC'],
    height=bar_height,
    color='#e9a23b',
    label='Test ROC AUC',
)
axis.axvline(0.85, color='#eff7f3', linestyle='--', linewidth=1.4, label='Test goal: 0.85')
axis.set_yticks(bar_positions, benchmarks['Model'])
axis.set_xlim(0.6, 0.9)
axis.set_xlabel('ROC AUC', color='#eff7f3')
axis.tick_params(colors='#eff7f3')
axis.grid(axis='x', color='#829690', alpha=0.25)
for spine in axis.spines.values():
    spine.set_color('#3b504b')
axis.invert_yaxis()
axis.legend(loc='lower right', frameon=False, ncols=3, labelcolor='#eff7f3')
figure.tight_layout()
st.pyplot(figure, width='stretch')
plt.close(figure)
st.dataframe(benchmarks.sort_values('Test ROC AUC', ascending=False), width='stretch', hide_index=True)

st.divider()
st.header('Exploratory charts')
exploratory_charts = [
    ('01 · Churn distribution', '01_churn_distribution_bar.png'),
    ('02 · Churn share', '02_churn_distribution_pie.png'),
    ('03 · Tenure by churn', '03_tenure_distribution_by_churn.png'),
    ('04 · Monthly charges by churn', '04_monthly_charges_distribution_by_churn.png'),
    ('05 · Feature correlation', '05_correlation_heatmap.png'),
]
for chart_title, filename in exploratory_charts:
    chart_path = PROJECT_ROOT / 'reports' / filename
    if chart_path.is_file():
        st.subheader(chart_title)
        st.image(str(chart_path), width='stretch')

st.divider()
st.header('Model evaluation')
if ROC_PLOT_PATH.is_file():
    st.subheader('06 · Held-out ROC curves')
    st.image(str(ROC_PLOT_PATH), width='stretch')

comparison_confusion_path = PROJECT_ROOT / 'reports' / '07_top_two_confusion_matrices.png'
if comparison_confusion_path.is_file():
    st.subheader('07 · Top two baseline confusion matrices')
    st.image(str(comparison_confusion_path), width='stretch')

confusion_path = PROJECT_ROOT / 'reports' / '08_tuned_model_confusion_matrix.png'
if confusion_path.is_file():
    st.subheader('08 · Tuned model confusion matrix')
    st.image(str(confusion_path), width='stretch')

st.divider()
st.header('Model explanations')
shap_path = PROJECT_ROOT / 'reports' / '09_shap_summary.png'
if shap_path.is_file():
    st.subheader('09 · SHAP global feature importance')
    st.image(str(shap_path), width='stretch')

waterfall_path = PROJECT_ROOT / 'reports' / '10_shap_waterfall_one_customer.png'
if waterfall_path.is_file():
    st.subheader('10 · SHAP explanation for one customer')
    st.image(str(waterfall_path), width='stretch')

st.info('Held-out test ROC AUC is 0.8476, below the requested > 0.85 goal. SHAP describes model associations, not causes.')