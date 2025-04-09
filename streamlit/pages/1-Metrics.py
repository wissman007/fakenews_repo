import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from google.oauth2 import service_account

st.set_page_config(page_title="Statistics & Metrics", layout="wide")

# Auth
gcp_secrets = st.secrets["gcp_service_account"]
dataset_info = st.secrets["id"]
project_id = gcp_secrets["project_id"]
dataset = dataset_info["dataset"]
table = dataset_info["table"]

credentials = service_account.Credentials.from_service_account_info(gcp_secrets)
client = bigquery.Client(credentials=credentials, project=project_id)

@st.cache_data(ttl=86400)
def get_data():
    query = f"SELECT * FROM `{project_id}.{dataset}.{table}`"
    df = client.query(query).to_dataframe()
    df['date_reference'] = pd.to_datetime(df['date_reference'])
    df['prediction'] = df['prediction'].str.strip()
    return df

df = get_data()

st.title("📊 News Statistics & Insights")
st.caption("A quick look at what's going on in the dataset.")

# 🔢 Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total News", f"{len(df):,}")
col2.metric("Fake News", f"{(df['prediction'] == 'fake news').sum()} ({(df['prediction'] == 'fake news').mean():.0%})")
col3.metric("Suspicious", f"{(df['prediction'] == 'Suspicious news').sum()}")
col4.metric("Trustworthy", f"{(df['prediction'].isin(['Real news', 'Trustful news']).sum())}")

st.markdown("---")

# 🔥 Bar chart
prediction_counts = df['prediction'].value_counts().reset_index()
prediction_counts.columns = ['prediction', 'count']

fig1 = px.bar(
    prediction_counts,
    x='prediction', y='count',
    title="Distribution of News Predictions",
    color='prediction',
    color_discrete_sequence=px.colors.sequential.Oranges
)
st.plotly_chart(fig1, use_container_width=True)

# 📈 Score over time
df_score = df.groupby(df['date_reference'].dt.date)['score'].mean().reset_index()
fig2 = px.line(
    df_score,
    x='date_reference', y='score',
    title="Average Prediction Score Over Time",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#FF4500"]
)
st.plotly_chart(fig2, use_container_width=True)
