---
title: ChurnSense Customer Retention
sdk: streamlit
sdk_version: 1.65.0
python_version: 3.13
app_file: app/streamlit_app.py
pinned: false
---

# Internship_Churnsense

Customer churn prediction project for the Telco Customer Churn dataset.

## Overview

This project analyzes customer churn and builds machine learning models to predict whether a customer will churn.

The workflow includes:
- data exploration and preprocessing
- feature engineering
- model comparison and evaluation
- reporting and documentation

## Project structure

```text
Internship_Churnsense/
├── data/
│   ├── raw/
│   │   └── Customer_churn.csv
│   └── processed/
├── models/
├── notebooks/
│   ├── 01_Project_Introduction.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Preprocessing_Feature_Engineering.ipynb
│   └── 04_Model_Building_Comparison.ipynb
├── reports/
├── src/
│   ├── __init__.py
│   ├── model.py
│   ├── preprocessing.py
│   └── utils.py
├── app/
│   ├── streamlit_app.py
│   ├── shared.py
│   └── pages/
│       ├── 1_Predict.py
│       ├── 2_Batch.py
│       ├── 3_Analytics.py
│       └── 4_Dashboard.py
├── tests/
│   ├── test_pipeline.py
│   └── fixtures/new_customers.csv
├── .gitignore
├── requirements.txt
├── README.md
└── .venv/
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Open the notebooks in order:
   - 01_Project_Introduction.ipynb
   - 02_EDA.ipynb
   - 03_Preprocessing_Feature_Engineering.ipynb
   - 04_Model_Building_Comparison.ipynb

## Production pipeline

The serialized pipeline at `models/churn_model_v1.pkl` includes the fitted
preprocessor and classifier. `src/preprocessing.py` validates raw customer
columns and recreates the engineered features expected by that artifact.
`src/model.py` loads the artifact and returns churn probabilities, decisions,
and risk bands. The app expects the same customer columns as the training data;
`customerID`, `Churn`, and other extra columns are not passed into the model.

Run the multi-page Streamlit app from the project root:

```bash
streamlit run app/streamlit_app.py
```

The local demo uses port 8501 by default. Hugging Face Spaces uses its Streamlit
SDK runtime; the Space configuration is declared in this README's front matter.

The app contains four pages: Dashboard, Predict, Batch, and Analytics. Batch
scoring accepts a CSV and offers a scored CSV download. A synthetic, separate
input file for a quick end-to-end check is available at
`tests/fixtures/new_customers.csv` and from the Batch page.

Run the pipeline tests with:

```bash
pytest
```

## Evaluation status

The tuned model achieved a held-out test ROC AUC of 0.8476. This is below the
project goal of greater than 0.85; training cross-validation results are not a
replacement for the held-out test score. See `reports/model_card.md` for
performance details and limitations.

## Notebook flow

- 01_Project_Introduction: project overview and goals
- 02_EDA: exploratory data analysis
- 03_Preprocessing_Feature_Engineering: cleaning, encoding, and feature engineering
- 04_Model_Building_Comparison: model selection and evaluation

## Requirements

The project dependencies are listed in [requirements.txt](requirements.txt).

## License

This project is for educational and internship use.
