"""Batch scoring page for customer CSV files."""

import streamlit as st

from app.shared import SAMPLE_CSV_PATH, get_model, page_header
from src.model import predict_customers
from src.utils import read_customer_csv

page_header('Portfolio assessment', 'Batch scoring', 'Customer file · scored records · export')

if SAMPLE_CSV_PATH.is_file():
    st.download_button(
        'Download synthetic sample CSV',
        data=SAMPLE_CSV_PATH.read_bytes(),
        file_name='new_customers_sample.csv',
        mime='text/csv',
    )

uploaded_file = st.file_uploader('Customer CSV', type=['csv'])
if uploaded_file is not None:
    try:
        customers = read_customer_csv(uploaded_file)
        with st.spinner('Scoring customer records...'):
            scored = predict_customers(customers, model=get_model())

        churn_count = int((scored['predicted_churn'] == 'Churn').sum())
        metric_cols = st.columns(3)
        metric_cols[0].metric('Records scored', f'{len(scored):,}')
        metric_cols[1].metric('Flagged at 50%', f'{churn_count:,}')
        metric_cols[2].metric('Average churn likelihood', f"{scored['churn_probability'].mean():.1%}")
        st.dataframe(scored, use_container_width=True, hide_index=True)
        st.download_button(
            'Download scored CSV',
            data=scored.to_csv(index=False).encode('utf-8'),
            file_name='churn_predictions.csv',
            mime='text/csv',
            type='primary',
        )
    except (UnicodeDecodeError, ValueError, TypeError, FileNotFoundError) as error:
        st.error(f'Unable to score this file: {error}')