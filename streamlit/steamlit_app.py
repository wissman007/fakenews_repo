import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
import plotly.express as px

# 🎨 Couleurs façon Reddit
PRIMARY_COLOR = "#FF4500"
BG_COLOR = "#F9F9F9"

# Configuration Streamlit
st.set_page_config(
    page_title="Reddit Style Fake News Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌈 CSS perso pour thème Reddit
st.markdown(f"""
    <style>
    body {{
        background-color: {BG_COLOR};
    }}
    .stApp {{
        font-family: 'Segoe UI', sans-serif;
    }}
    .main > div {{
        padding-top: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# 🔐 Auth GCP
gcp_secrets = st.secrets["gcp_service_account"]
dataset_info = st.secrets["id"]
project_id = gcp_secrets["project_id"]
dataset = dataset_info["dataset"]
table = dataset_info["table"]

# Connexion
credentials = service_account.Credentials.from_service_account_info(gcp_secrets)
client = bigquery.Client(credentials=credentials, project=project_id)

# 🔁 Chargement avec cache
@st.cache_data(ttl=86400)
def get_data():
    query = f"SELECT * FROM `{project_id}.{dataset}.{table}`"
    df = client.query(query).to_dataframe()
    df['date_reference'] = pd.to_datetime(df['date_reference'])
    df['prediction'] = df['prediction'].str.strip()  # nettoyage
    return df

# 📤 Rafraîchissement
if st.sidebar.button("🔁 Rafraîchir maintenant"):
    st.cache_data.clear()

df = get_data()

# 🎯 Métriques
col1, col2, col3, col4 = st.columns(4)
col1.metric("📰 Total News", f"{len(df):,}")
col2.metric("🕵️‍♀️ Fake News", f"{(df['prediction'] == 'fake news').sum()} ({(df['prediction'] == 'fake news').mean():.0%})")
col3.metric("😐 Suspicious", f"{(df['prediction'] == 'Suspicious news').sum()}")
col4.metric("✅ Réelles/Fiables", f"{(df['prediction'].isin(['Real news', 'Trustful news']).sum())}")

st.markdown("---")

# 📊 Graphe de répartition des prédictions
prediction_counts = df['prediction'].value_counts().reset_index()
prediction_counts.columns = ['prediction', 'count']  # 👈 renommage explicite

fig1 = px.bar(
    prediction_counts,
    x='prediction', y='count',
    labels={'prediction': 'Type de news', 'count': 'Nombre'},
    color='prediction',
    color_discrete_sequence=px.colors.sequential.Oranges,
    title="Répartition des types de prédictions"
)
st.plotly_chart(fig1, use_container_width=True)

# 📈 Score moyen par jour
df_score_by_day = df.groupby(df['date_reference'].dt.date)['score'].mean().reset_index()
fig2 = px.line(
    df_score_by_day,
    x='date_reference', y='score',
    title='Évolution du score moyen au fil du temps',
    markers=True,
    line_shape="spline",
    color_discrete_sequence=[PRIMARY_COLOR]
)
st.plotly_chart(fig2, use_container_width=True)

# 🧾 Données filtrables
st.markdown("### 🔍 Aperçu des données")
with st.expander("📂 Filtrer les données"):
    sources = st.multiselect("Source(s)", df['source'].unique(), default=list(df['source'].unique()))
    auteurs = st.multiselect("Auteur(s)", df['author'].unique(), default=list(df['author'].unique()))
    predictions = st.multiselect("Type de prédiction", df['prediction'].unique(), default=list(df['prediction'].unique()))
    df_filtered = df[df['source'].isin(sources) & df['author'].isin(auteurs) & df['prediction'].isin(predictions)]

st.dataframe(df_filtered.sort_values(by="date_reference", ascending=False), use_container_width=True)
# 📥 Exporter les données
st.download_button(
    label="📥 Exporter les données",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name='filtered_data.csv',
    mime='text/csv'
)
# 📚 Documentation
st.markdown("---")
st.markdown("### 📚 Documentation")
st.markdown("""
    Ce tableau de bord permet d'analyser les prédictions de fake news à partir de données stockées dans BigQuery.
    - **Total News** : Nombre total de nouvelles.
    - **Fake News** : Nombre et pourcentage de nouvelles considérées comme fausses.
    - **Suspicious** : Nombre de nouvelles considérées comme suspectes.
    - **Réelles/Fiables** : Nombre de nouvelles considérées comme réelles ou fiables.
    - **Répartition des types de prédictions** : Graphique montrant la répartition des différentes catégories de nouvelles.
    - **Évolution du score moyen au fil du temps** : Graphique montrant l'évolution du score moyen des nouvelles au fil du temps.
    - **Filtrer les données** : Options pour filtrer les données par source, auteur et type de prédiction.
    - **Exporter les données** : Option pour télécharger les données filtrées au format CSV.
    """)
# Footer
st.markdown("---")
st.markdown(
    """
    <style>
        footer {
            visibility: hidden;
        }
        .stApp {
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)