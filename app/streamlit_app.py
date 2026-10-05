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
        --ink: #eff7f3;
        --muted: #b3c5bf;
        --paper: #101918;
        --surface: #1c2927;
        --raised: #253633;
        --border: #3b504b;
        --teal: #42d6b5;
        --amber: #f2b15b;
    }
    html, body, .stApp, [data-testid="stMarkdownContainer"] {
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0;
        color: var(--ink);
    }
    [data-testid="stAppViewContainer"], [data-testid="stMain"], .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] small,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] { color: var(--ink); }
    [data-testid="stSidebar"] { background: #172421; }
    [data-testid="stSidebar"] * { color: #eff7f3; }
    [data-testid="stSidebarNav"] { padding-top: 1rem; }
    h1, h2, h3, h4 { color: var(--ink); font-family: 'Manrope', sans-serif; letter-spacing: 0; }
    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--teal);
        border-radius: 4px;
        padding: 1rem 1.1rem;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: var(--ink); }
    .page-subtitle { color: var(--muted) !important; margin-top: -0.65rem; margin-bottom: 1.5rem; }
    .app-title {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid var(--border);
    }
    div[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 1.2rem; }
    input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {
        background-color: var(--raised) !important;
        color: var(--ink) !important;
        border-color: var(--border) !important;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] { background: var(--surface); }
    [data-testid="stAlert"] p { color: var(--ink); }
    div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button {
        background: #087e73; color: #ffffff; border: 1px solid #42d6b5; border-radius: 4px; font-weight: 700;
    }
    div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover {
        background: #06675f; color: #ffffff; border-color: #72e5ca;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-title">Churnsense - Customer Retention Intelligence</div>',
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