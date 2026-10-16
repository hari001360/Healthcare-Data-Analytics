# Healthcare Data Analytics

A data analytics project on 55,500 inpatient hospital records to explore clinical trends, billing patterns, and patient insights.

---

## Files

- `healthcare_dataset.csv` – Raw dataset
- `healthcare_dataset_cleaned.csv` – Cleaned dataset
- `healthcare_data_analysis.ipynb` – Data analysis notebook
- `healthcare_sql_analytics.sql` – SQL queries
- `dashboard.py` – Streamlit dashboard
- `generate_report.py` – PDF report generator
- `Healthcare_Analytics_Report.pdf` – Final report

---

## Dataset

- **55,500** patient records
- **15** features: Name, Age, Gender, Blood Type, Medical Condition, Admission Type, Hospital, Doctor, Insurance Provider, Billing Amount, Medication, Test Results, and more
- **Conditions:** Arthritis, Diabetes, Hypertension, Obesity, Cancer, Asthma

---

## How to Run

**Install dependencies**
```bash
pip install streamlit plotly pandas matplotlib fpdf2
```

**Run the dashboard**
```bash
streamlit run dashboard.py
```

**Generate PDF report**
```bash
python generate_report.py
```

---

## Tools Used

- Python, Pandas
- Streamlit, Plotly
- Matplotlib, SQL

