"""Model performance and explainability page."""

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
figure, axis = plt.subplots(figsize=(10, 5.2))
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
axis.axvline(0.85, color='#172b2a', linestyle='--', linewidth=1.4, label='Test goal: 0.85')
axis.set_yticks(bar_positions, benchmarks['Model'])
axis.set_xlim(0.6, 0.9)
axis.set_xlabel('ROC AUC')
axis.grid(axis='x', alpha=0.2)
axis.invert_yaxis()
axis.legend(loc='lower right', frameon=False, ncols=3)
figure.tight_layout()
st.pyplot(figure, use_container_width=True)
plt.close(figure)
st.dataframe(benchmarks.sort_values('Test ROC AUC', ascending=False), use_container_width=True, hide_index=True)

if ROC_PLOT_PATH.is_file():
    st.subheader('Held-out ROC curves')
    st.image(str(ROC_PLOT_PATH), use_container_width=True)

confusion_path = PROJECT_ROOT / 'reports' / '08_tuned_model_confusion_matrix.png'
shap_path = PROJECT_ROOT / 'reports' / '09_shap_summary.png'
visual_cols = st.columns(2)
with visual_cols[0]:
    if confusion_path.is_file():
        st.subheader('Tuned model · confusion matrix')
        st.image(str(confusion_path), use_container_width=True)
with visual_cols[1]:
    if shap_path.is_file():
        st.subheader('SHAP · global importance')
        st.image(str(shap_path), use_container_width=True)

st.info('Held-out test ROC AUC is 0.8476, below the requested > 0.85 goal. SHAP describes model associations, not causes.')