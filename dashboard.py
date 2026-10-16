import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Dashboard", page_icon="🏥", layout="wide")

# ── Load & prepare data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("healthcare_dataset.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["date_of_admission"] = pd.to_datetime(df["date_of_admission"], errors="coerce")
    df["discharge_date"]    = pd.to_datetime(df["discharge_date"],    errors="coerce")
    df["length_of_stay"]    = (df["discharge_date"] - df["date_of_admission"]).dt.days.clip(lower=0)
    df["billing_amount"]    = pd.to_numeric(df["billing_amount"], errors="coerce")
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🏥 Filters")
sel_condition = st.sidebar.multiselect("Medical Condition", sorted(df["medical_condition"].unique()), default=sorted(df["medical_condition"].unique()))
sel_gender    = st.sidebar.multiselect("Gender",            sorted(df["gender"].unique()),            default=sorted(df["gender"].unique()))
sel_admission = st.sidebar.multiselect("Admission Type",    sorted(df["admission_type"].unique()),    default=sorted(df["admission_type"].unique()))

fdf = df[
    df["medical_condition"].isin(sel_condition) &
    df["gender"].isin(sel_gender) &
    df["admission_type"].isin(sel_admission)
]

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🏥 Healthcare Analytics Dashboard")
st.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** records")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Patients",    f"{len(fdf):,}")
k2.metric("Total Revenue",     f"${fdf[fdf['billing_amount']>0]['billing_amount'].sum()/1e6:.1f}M")
k3.metric("Avg. Billing",      f"${fdf['billing_amount'].mean():,.0f}")
k4.metric("Avg. Stay",         f"{fdf['length_of_stay'].mean():.1f} days")
k5.metric("Avg. Age",          f"{fdf['age'].mean():.1f} yrs")
k6.metric("Abnormal Tests",    f"{(fdf['test_results']=='Abnormal').mean()*100:.1f}%")

st.divider()

# ── Row 1: Conditions | Admission Types ──────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Patients by Medical Condition")
    cond_df = fdf["medical_condition"].value_counts().reset_index()
    cond_df.columns = ["Condition", "Patients"]
    fig = px.bar(cond_df, x="Condition", y="Patients", color="Condition", text="Patients")
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Admission Type Split")
    adm_df = fdf["admission_type"].value_counts().reset_index()
    adm_df.columns = ["Type", "Count"]
    fig = px.pie(adm_df, names="Type", values="Count", hole=0.4)
    fig.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Insurance Revenue | Test Results ───────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Revenue by Insurance Provider")
    ins_df = fdf[fdf["billing_amount"] > 0].groupby("insurance_provider")["billing_amount"].sum().reset_index()
    ins_df.columns = ["Insurer", "Revenue"]
    ins_df = ins_df.sort_values("Revenue", ascending=False)
    fig = px.bar(ins_df, x="Insurer", y="Revenue", color="Insurer", text=ins_df["Revenue"].apply(lambda x: f"${x/1e6:.1f}M"))
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Test Results Distribution")
    tr_df = fdf["test_results"].value_counts().reset_index()
    tr_df.columns = ["Result", "Count"]
    colors = {"Normal": "#22c55e", "Abnormal": "#ef4444", "Inconclusive": "#f59e0b"}
    fig = px.pie(tr_df, names="Result", values="Count", hole=0.4,
                 color="Result", color_discrete_map=colors)
    fig.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Avg Billing by Condition | Monthly Trend ──────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("Avg. Billing by Condition")
    avg_df = fdf.groupby("medical_condition")["billing_amount"].mean().reset_index()
    avg_df.columns = ["Condition", "Avg Billing"]
    avg_df = avg_df.sort_values("Avg Billing", ascending=True)
    fig = px.bar(avg_df, x="Avg Billing", y="Condition", orientation="h",
                 color="Condition", text=avg_df["Avg Billing"].apply(lambda x: f"${x:,.0f}"))
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Monthly Admissions Trend")
    fdf["month"] = fdf["date_of_admission"].dt.to_period("M").astype(str)
    trend = fdf.groupby("month").size().reset_index(name="Admissions")
    trend = trend.sort_values("month")
    fig = px.line(trend, x="month", y="Admissions", markers=True)
    fig.update_layout(margin=dict(t=10, b=10))
    fig.update_xaxes(tickangle=45, nticks=15)
    st.plotly_chart(fig, use_container_width=True)

st.caption("Healthcare Analytics · 55,500 patient records · Built with Streamlit & Plotly")
