"""ChurnSense multi-page Streamlit application entry point."""

import streamlit as st

st.set_page_config(
    page_title='ChurnSense | Customer Retention',
    page_icon='C',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    :root {
        --ink: #172b2a;
        --muted: #607472;
        --paper: #f3f6f3;
        --teal: #087e73;
        --mint: #d8eee6;
        --amber: #e9a23b;
    }
    html, body, [class*="st-"], [data-testid="stMarkdownContainer"] {
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0;
    }
    [data-testid="stAppViewContainer"] { background: var(--paper); }
    [data-testid="stSidebar"] { background: #172b2a; }
    [data-testid="stSidebar"] * { color: #eef6f1; }
    [data-testid="stSidebarNav"] { padding-top: 1rem; }
    h1, h2, h3 { color: var(--ink); font-family: 'Manrope', sans-serif; letter-spacing: 0; }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce6df;
        border-left: 4px solid var(--teal);
        border-radius: 4px;
        padding: 1rem 1.1rem;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    .page-subtitle { color: var(--muted); margin-top: -0.65rem; margin-bottom: 1.5rem; }
    div[data-testid="stForm"] { background: #ffffff; border: 1px solid #dce6df; border-radius: 4px; padding: 1.2rem; }
    div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button {
        background: var(--teal); color: white; border: 0; border-radius: 4px; font-weight: 700;
    }
    div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover {
        background: #06675f; color: white; border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('## CHURNSENSE')
st.sidebar.caption('CUSTOMER RETENTION INTELLIGENCE')

dashboard = st.Page('pages/4_Dashboard.py', title='Dashboard', default=True)
predict = st.Page('pages/1_Predict.py', title='Predict')
batch = st.Page('pages/2_Batch.py', title='Batch')
analytics = st.Page('pages/3_Analytics.py', title='Analytics')
page = st.navigation({'WORKSPACE': [dashboard, predict, batch, analytics]})
page.run()