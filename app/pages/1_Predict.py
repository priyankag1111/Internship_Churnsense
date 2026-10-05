"""Single-customer churn prediction page."""

import pandas as pd
import streamlit as st

from app.shared import get_model, page_header
from src.model import predict_customers

page_header('Individual assessment', 'Customer prediction', 'Customer profile · model assessment')

with st.form('customer_prediction'):
    identity_col, tenure_col, spend_col = st.columns(3)
    with identity_col:
        customer_id = st.text_input('Customer ID', value='NEW-CUSTOMER')
        gender = st.selectbox('Gender', ['Female', 'Male', 'Nonbinary'])
        senior_citizen = st.selectbox(
            'Senior citizen', [0, 1],
            format_func=lambda value: 'Yes' if value else 'No',
        )
        partner = st.selectbox('Partner', ['No', 'Yes'])
        dependents = st.selectbox('Dependents', ['No', 'Yes'])
    with tenure_col:
        tenure = st.number_input('Tenure (months)', min_value=0, max_value=100, value=12, step=1)
        phone_service = st.selectbox('Phone service', ['Yes', 'No'])
        internet_service = st.selectbox('Internet service', ['Fiber optic', 'DSL', 'No'])
        contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
        paperless_billing = st.selectbox('Paperless billing', ['Yes', 'No'])
    with spend_col:
        monthly_charges = st.number_input('Monthly charges ($)', min_value=0.0, value=75.0, step=5.0)
        total_charges_missing = st.checkbox('Total charges unavailable')
        total_charges = st.number_input(
            'Total charges ($)', min_value=0.0, value=900.0, step=50.0,
            disabled=total_charges_missing,
        )
        payment_method = st.selectbox('Payment method', [
            'Electronic check', 'Mailed check', 'Bank transfer (automatic)',
            'Credit card (automatic)',
        ])
        threshold = st.slider('Decision threshold', min_value=0.10, max_value=0.90, value=0.50, step=0.05)

    service_values = ['No internet service'] if internet_service == 'No' else ['No', 'Yes']
    phone_line_values = ['No phone service'] if phone_service == 'No' else ['No', 'Yes']
    service_col1, service_col2, service_col3 = st.columns(3)
    with service_col1:
        multiple_lines = st.selectbox('Multiple lines', phone_line_values)
        online_security = st.selectbox('Online security', service_values)
    with service_col2:
        online_backup = st.selectbox('Online backup', service_values)
        device_protection = st.selectbox('Device protection', service_values)
    with service_col3:
        tech_support = st.selectbox('Tech support', service_values)
        streaming_tv = st.selectbox('Streaming TV', service_values)
        streaming_movies = st.selectbox('Streaming movies', service_values)

    submitted = st.form_submit_button('Assess churn risk', use_container_width=True)

if submitted:
    customer = pd.DataFrame([{
        'customerID': customer_id,
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': None if total_charges_missing else total_charges,
    }])
    try:
        result = predict_customers(customer, model=get_model(), threshold=threshold).iloc[0]
        probability = float(result['churn_probability'])
        result_col, detail_col = st.columns([1, 2])
        with result_col:
            st.metric('Churn likelihood', f'{probability:.1%}')
            st.progress(probability)
        with detail_col:
            st.subheader(f"{result['risk_level']} risk")
            if result['predicted_churn'] == 'Churn':
                st.warning(f"The model flags {customer_id} above the {threshold:.0%} decision threshold.")
            else:
                st.success(f"The model places {customer_id} below the {threshold:.0%} decision threshold.")
            st.caption('This score is a prioritization signal, not a causal explanation or guarantee.')
    except (TypeError, ValueError, FileNotFoundError) as error:
        st.error(str(error))