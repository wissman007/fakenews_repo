import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

st.set_page_config(
    page_title="Fake News Dashboard",
    layout="wide"
)

#Welcoming message 
st.title("Welcome to the Reddit Fake News Detector!")
st.markdown("""
This dashboard provides real-time insights into the classification of [r/worldnews](https://www.reddit.com/r/worldnews/new/) articles.
The data is refreshed every 24 hours.
""")

# 🎨 Header
st.title("📰 Live News Table")
st.caption("Real-time data from Google BigQuery – refreshed every 24h.")

# 🔐 Authentification GCP
gcp_secrets = st.secrets["gcp_service_account"]
dataset_info = st.secrets["id"]
project_id = gcp_secrets["project_id"]
dataset = dataset_info["dataset"]
table = dataset_info["table"]

credentials = service_account.Credentials.from_service_account_info(gcp_secrets)
client = bigquery.Client(credentials=credentials, project=project_id)

# 📥 Chargement des données
@st.cache_data(ttl=86400)
def get_data():
    query = f"SELECT title, date_reference, scrapping_status, score, prediction, url FROM `{project_id}.{dataset}.{table}`"
    df = client.query(query).to_dataframe()
    df['date_reference'] = pd.to_datetime(df['date_reference'])
    df['prediction'] = df['prediction'].str.strip()
    df.columns = ['Title', 'Date', 'Status', 'Score', 'Prediction','URL']
    return df

# 🔁 Rafraîchissement manuel
if st.sidebar.button("🔁 Refresh data"):
    st.cache_data.clear()

df = get_data()

# 🎛 Filtres dynamiques
with st.expander("🔎 Filter options"):
    predictions = st.multiselect(
        "Select News Type(s)", 
        options=df['Prediction'].unique(), 
        default=list(df['Prediction'].unique())
    )
    df = df[df['Prediction'].isin(predictions)]

# 📋 Affichage du tableau
st.data_editor(
    df,
    column_config={
        "URL": st.column_config.LinkColumn(
            "Title",  # Le nom de la colonne dans le tableau
            display_text=f"{df['Title']}",  # Utilise le titre du DataFrame comme texte du lien
        )
    },
    column_order=["URL", "Date", "Scrapping Status", "Score", "Prediction"],
    hide_index=True,
    use_container_width=True
)

