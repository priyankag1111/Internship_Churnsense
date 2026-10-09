"""Historical churn overview dashboard."""

import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import altair as alt
import pandas as pd
import streamlit as st

from app.shared import get_reference_data, page_header

page_header('Portfolio overview', 'Customer pulse', 'Telco customer cohort · historical churn')

customers = get_reference_data().copy()
if 'Churn' not in customers.columns:
    st.error('The reference dataset must contain the Churn column.')
    st.stop()

churned = customers['Churn'].eq('Yes')
churn_rate = float(churned.mean())
metric_cols = st.columns(4)
metric_cols[0].metric('Customers', f'{len(customers):,}')
metric_cols[1].metric('Churned', f'{int(churned.sum()):,}')
metric_cols[2].metric('Churn rate', f'{churn_rate:.1%}')
metric_cols[3].metric(
    'Average monthly charge',
    f"${pd.to_numeric(customers['MonthlyCharges'], errors='coerce').mean():.2f}",
)

contract_summary = (
    customers.assign(_churn=churned)
    .groupby('Contract', observed=True)
    .agg(Customers=('_churn', 'size'), Churned=('_churn', 'sum'), Churn_rate=('_churn', 'mean'))
    .reset_index()
)
contract_chart = (
    alt.Chart(contract_summary)
    .mark_bar(color='#087e73')
    .encode(
        x=alt.X('Contract:N', sort=['Month-to-month', 'One year', 'Two year'], title='Contract'),
        y=alt.Y('Churn_rate:Q', axis=alt.Axis(format='.0%'), title='Customers churned (%)'),
        tooltip=[
            alt.Tooltip('Contract:N', title='Contract'),
            alt.Tooltip('Customers:Q', title='Customers', format=','),
            alt.Tooltip('Churned:Q', title='Churned', format=','),
            alt.Tooltip('Churn_rate:Q', title='Churn rate', format='.1%'),
        ],
    )
    .properties(height=320)
)
contract_labels = contract_chart.mark_text(dy=-10, color='#eff7f3', fontWeight='bold').encode(
    text=alt.Text('Churn_rate:Q', format='.1%')
)

outcome_summary = (
    customers['Churn']
    .value_counts()
    .rename(index={'No': 'Stayed', 'Yes': 'Churned'})
    .rename_axis('Outcome')
    .rename('Customers')
    .reset_index()
)
outcome_summary['Share'] = outcome_summary['Customers'] / len(customers)
outcome_summary['Label'] = outcome_summary.apply(
    lambda row: f"{row['Customers']:,} ({row['Share']:.1%})",
    axis=1,
)
outcome_chart = (
    alt.Chart(outcome_summary)
    .mark_bar()
    .encode(
        x=alt.X('Outcome:N', sort=['Churned', 'Stayed'], title='Customer outcome'),
        y=alt.Y('Customers:Q', title='Customers'),
        color=alt.Color(
            'Outcome:N',
            scale=alt.Scale(domain=['Stayed', 'Churned'], range=['#087e73', '#e9a23b']),
            legend=None,
        ),
        tooltip=[
            alt.Tooltip('Outcome:N', title='Outcome'),
            alt.Tooltip('Customers:Q', title='Customers', format=','),
            alt.Tooltip('Share:Q', title='Share of customers', format='.1%'),
        ],
    )
    .properties(height=320)
)
outcome_labels = outcome_chart.mark_text(dy=-10, color='#eff7f3', fontWeight='bold').encode(
    text=alt.Text('Label:N')
)

chart_cols = st.columns(2)
with chart_cols[0]:
    st.subheader('Churn by contract')
    st.altair_chart(contract_chart + contract_labels, width='stretch')
with chart_cols[1]:
    st.subheader('Customer outcomes')
    st.altair_chart(outcome_chart + outcome_labels, width='stretch')

highest_contract = contract_summary.loc[contract_summary['Churn_rate'].idxmax()]
lowest_contract = contract_summary.loc[contract_summary['Churn_rate'].idxmin()]
st.markdown(
    '**Business insights**\n\n'
    f"- **Churn by contract:** {highest_contract['Contract']} customers have the highest "
    f"churn rate ({highest_contract['Churn_rate']:.1%}); {lowest_contract['Contract']} "
    f"customers have the lowest ({lowest_contract['Churn_rate']:.1%}). "
    'Consider prioritizing retention efforts for month-to-month customers.\n'
    f"- **Customer outcomes:** {churn_rate:.1%} of customers churned "
    f"({int(churned.sum()):,} of {len(customers):,}); the remaining "
    f"{1 - churn_rate:.1%} stayed."
)

st.subheader('Tenure profile')
tenure = pd.to_numeric(customers['tenure'], errors='coerce')
tenure_bands = pd.cut(
    tenure,
    bins=[-1, 6, 12, 24, 48, 72],
    labels=['0–6', '7–12', '13–24', '25–48', '49–72'],
)
tenure_summary = (
    customers.assign(_tenure_band=tenure_bands, _churn=churned)
    .groupby('_tenure_band', observed=True)
    .agg(Customers=('_churn', 'size'), Churned=('_churn', 'sum'), Churn_rate=('_churn', 'mean'))
    .reset_index()
    .rename(columns={'_tenure_band': 'Tenure'})
)
tenure_summary['Tenure'] = tenure_summary['Tenure'].astype(str)
tenure_chart = (
    alt.Chart(tenure_summary)
    .mark_bar(color='#e9a23b')
    .encode(
        x=alt.X(
            'Tenure:N',
            sort=['0–6', '7–12', '13–24', '25–48', '49–72'],
            title='Tenure (months)',
        ),
        y=alt.Y('Churn_rate:Q', axis=alt.Axis(format='.0%'), title='Customers churned (%)'),
        tooltip=[
            alt.Tooltip('Tenure:N', title='Tenure (months)'),
            alt.Tooltip('Customers:Q', title='Customers', format=','),
            alt.Tooltip('Churned:Q', title='Churned', format=','),
            alt.Tooltip('Churn_rate:Q', title='Churn rate', format='.1%'),
        ],
    )
    .properties(height=320)
)
tenure_labels = tenure_chart.mark_text(dy=-10, color='#eff7f3', fontWeight='bold').encode(
    text=alt.Text('Churn_rate:Q', format='.1%')
)
st.altair_chart(tenure_chart + tenure_labels, width='stretch')

highest_tenure_churn = tenure_summary.loc[tenure_summary['Churn_rate'].idxmax()]
lowest_tenure_churn = tenure_summary.loc[tenure_summary['Churn_rate'].idxmin()]
st.markdown(
    '**Business insights**\n\n'
    f"- Customers with **{highest_tenure_churn['Tenure']} months of tenure** have the "
    f"highest churn rate ({highest_tenure_churn['Churn_rate']:.1%}).\n"
    f"- Churn rate generally declines with tenure, reaching "
    f"{lowest_tenure_churn['Churn_rate']:.1%} in the "
    f"**{lowest_tenure_churn['Tenure']} months** band; early-tenure onboarding and "
    'support are useful retention focus areas.'
)
