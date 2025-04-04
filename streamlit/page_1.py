import streamlit as st
# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import random

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    st.write(rows_raw)
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


@st.cache_data(ttl=600)
def bq_to_df():
    sql = """
            SELECT * FROM `nlpfakenews.fake_news_detection.training_data` LIMIT 10
        """
    df = client.query_and_wait(sql).to_dataframe()
    return df

def write_random_article():
    my_df = st.session_state['df']
    rand = random.randint(0, len(my_df)-1)
    st.write(my_df[my_df.index==rand and my_df.any()])

def print_st():
    st.write(st.session_state['df'])

if "df" not in st.session_state:
    st.session_state["df"] = bq_to_df()
bq_to_df()
st.dataframe(st.session_state['df'])
if st.button("random news"):
    write_random_article()

#rows = run_query("SELECT * FROM `nlpfakenews.fake_news_detection.training_data` LIMIT 10")

