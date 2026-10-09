"""Model performance and explainability page."""

import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image, ImageOps

from app.shared import get_benchmarks, page_header
from src.utils import PROJECT_ROOT, ROC_PLOT_PATH


def display_chart_pair(chart_pair, columns):
    chart_images = []
    for chart_title, chart_path in chart_pair:
        if chart_path.is_file():
            with Image.open(chart_path) as image:
                chart_images.append((chart_title, image.convert('RGB')))
        else:
            chart_images.append((chart_title, None))

    available_images = [image for _, image in chart_images if image is not None]
    if not available_images:
        return

    canvas_size = (
        max(image.width for image in available_images),
        max(image.height for image in available_images),
    )
    for (chart_title, image), column in zip(chart_images, columns):
        if image is None:
            continue
        with column:
            st.subheader(chart_title)
            padded_image = ImageOps.pad(image, canvas_size, color='white')
            st.image(padded_image, width='stretch')
            padded_image.close()
        image.close()


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
axis.legend(
    loc='lower center',
    bbox_to_anchor=(0.5, 1.02),
    frameon=False,
    ncols=3,
    labelcolor='#eff7f3',
)
figure.tight_layout(rect=(0, 0, 1, 0.88))
st.pyplot(figure, width='stretch')
plt.close(figure)
st.dataframe(benchmarks.sort_values('Test ROC AUC', ascending=False), width='stretch', hide_index=True)
st.markdown(
    '**Business insights**\n\n'
    '- Tuned Gradient Boosting has the strongest held-out ROC AUC (0.8476), '
    'but it remains below the >0.85 goal; the CV score is 0.8509.\n'
    '- Gradient Boosting (0.8428) and Logistic Regression (0.8416) are the '
    'strongest baseline test performers, while Decision Tree is weakest (0.6296).'
)

st.divider()
st.header('Exploratory charts')
exploratory_chart_pairs = [
    (
        ('01 · Churn distribution', '01_churn_distribution_bar.png'),
        ('02 · Churn share', '02_churn_distribution_pie.png'),
    ),
    (
        ('03 · Tenure by churn', '03_tenure_distribution_by_churn.png'),
        ('04 · Monthly charges by churn', '04_monthly_charges_distribution_by_churn.png'),
    ),
]
for chart_pair_index, chart_pair in enumerate(exploratory_chart_pairs):
    display_chart_pair(
        [(title, PROJECT_ROOT / 'reports' / filename) for title, filename in chart_pair],
        st.columns(2),
    )
    if chart_pair_index == 0:
        st.markdown(
            '**Business insights**\n\n'
            '- **01 · Churn distribution:** 1,869 of 7,043 customers churned, '
            'so retention activity has a sizable addressable cohort.\n'
            '- **02 · Churn share:** churn is 26.5% of the cohort; most customers '
            'stayed, so account for this class imbalance when evaluating outreach or model results.'
        )
    else:
        st.markdown(
            '**Business insights**\n\n'
            '- **03 · Tenure by churn:** churn is concentrated among newer customers, '
            'while non-churners are more represented at longer tenures.\n'
            '- **04 · Monthly charges by churn:** churners are more concentrated at '
            'higher monthly charges, although the two distributions overlap.'
        )

correlation_path = PROJECT_ROOT / 'reports' / '05_correlation_heatmap.png'
if correlation_path.is_file():
    correlation_columns = st.columns([1, 8, 1])
    with correlation_columns[1]:
        st.subheader('05 · Feature correlation')
        st.image(str(correlation_path), width='stretch')
    st.markdown(
        '**Business insights**\n\n'
        '- Tenure and total charges have the strongest off-diagonal correlation (0.83); '
        'monthly and total charges are also correlated (0.65).\n'
        '- Churn has a moderate negative correlation with tenure (-0.35); these are '
        'associations, not evidence of causation.'
    )

st.divider()
st.header('Model evaluation')
if ROC_PLOT_PATH.is_file():
    roc_columns = st.columns([1, 8, 1])
    with roc_columns[1]:
        st.subheader('06 · Held-out ROC curves')
        st.image(str(ROC_PLOT_PATH), width='stretch')
    st.markdown(
        '**Business insights**\n\n'
        '- Gradient Boosting (AUC 0.843) and Logistic Regression (0.842) '
        'rank highest among the plotted baselines and perform similarly.\n'
        '- Every baseline is above chance, but none reaches the >0.85 target; '
        'the Decision Tree is weakest (AUC 0.630).'
    )

comparison_confusion_path = PROJECT_ROOT / 'reports' / '07_top_two_confusion_matrices.png'
confusion_path = PROJECT_ROOT / 'reports' / '08_tuned_model_confusion_matrix.png'
display_chart_pair(
    [
        ('07 · Top two baseline confusion matrices', comparison_confusion_path),
        ('08 · Tuned model confusion matrix', confusion_path),
    ],
    st.columns(2),
)
st.markdown(
    '**Business insights**\n\n'
    '- **07 · Baseline comparison:** Gradient Boosting and Logistic Regression '
    'have similar errors; Logistic Regression identifies 4 more churners '
    '(198 vs. 194) and produces 3 fewer false alarms (100 vs. 103) on this test split.\n'
    '- **08 · Tuned model:** it correctly identifies 198 of 374 churners, '
    'but misses 176; consider the cost of missed churn when selecting an operating threshold.'
)

st.divider()
st.header('Model explanations')
shap_path = PROJECT_ROOT / 'reports' / '09_shap_summary.png'
waterfall_path = PROJECT_ROOT / 'reports' / '10_shap_waterfall_one_customer.png'
display_chart_pair(
    [
        ('09 · SHAP global feature importance', shap_path),
        ('10 · SHAP explanation for one customer', waterfall_path),
    ],
    st.columns(2),
)
st.markdown(
    '**Business insights**\n\n'
    '- **09 · Global SHAP:** tenure-to-monthly-charge ratio is the strongest '
    'displayed feature; month-to-month contract, fiber-optic service, and lack '
    'of support/security services also contribute to model output. These are associations, not causes.\n'
    '- **10 · One-customer SHAP:** the example has a predicted churn probability '
    'of 91.5%; tenure-to-monthly-charge ratio is its largest upward contribution. '
    'This explains one prediction and should not be generalized to all customers.'
)

st.info('Held-out test ROC AUC is 0.8476, below the requested > 0.85 goal. SHAP describes model associations, not causes.')