"""Historical churn overview dashboard."""

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

chart_cols = st.columns([1.2, 1])
with chart_cols[0]:
    st.subheader('Churn by contract')
    contract_rates = customers.assign(_churn=churned).groupby('Contract', observed=True)['_churn'].mean()
    st.bar_chart(contract_rates.rename('Churn rate'), y_label='Churn rate', color='#087e73')
with chart_cols[1]:
    st.subheader('Customer outcomes')
    outcome_counts = customers['Churn'].value_counts().rename(index={'No': 'Stayed', 'Yes': 'Churned'})
    st.bar_chart(outcome_counts.rename('Customers'), color='#e9a23b')

st.subheader('Tenure profile')
tenure = pd.to_numeric(customers['tenure'], errors='coerce')
tenure_bands = pd.cut(
    tenure,
    bins=[-1, 6, 12, 24, 48, 72],
    labels=['0–6', '7–12', '13–24', '25–48', '49+'],
)
tenure_profile = pd.crosstab(tenure_bands, customers['Churn'], normalize='index')
st.bar_chart(tenure_profile.rename(columns={'No': 'Stayed', 'Yes': 'Churned'}), y_label='Share of customers')