import datetime
import sys
import os
import time
import requests
import json
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from pprint import pprint
from airflow.decorators import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateTableOperator, BigQueryInsertJobOperator, BigQueryCreateEmptyDatasetOperator, BigQueryUpsertTableOperator
sys.path.append("/opt/airflow")
from scripts.main import main

DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_NAME = "predicted_news"
TABLE_NAME_DATA_TO_MODEL = "training_data"
#PROJECT_NAME = os.get("PROJECT_NAME")
PROJECT_NAME="nlpfakenews"

def create_bq_retrieve_data_query(timestamp_min):
    query = f"""
        SELECT * 
        FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME_DATA_TO_MODEL}`
        LIMIT 3
    """
    return query


def mapping_score(score):
    if 0 <= score < 0.25:
        value = "fake news" 
    elif 0.25 <= score < 0.50:
        value = "Suspicious news " 
    elif 0.5 <= score < 0.75:
        value = "Trustful news"
    else:
        value = "Real news "    
    return value

with DAG(
    dag_id="test_dag_testing",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
) as dag:
    create_dataset = BigQueryCreateEmptyDatasetOperator(gcp_conn_id= "gcp_conn",task_id="create_dataset", dataset_id=DATASET_NAME)
    create_table = BigQueryCreateTableOperator(
        gcp_conn_id= "gcp_conn",
        task_id="create_table_intermediaire",
        dataset_id=DATASET_NAME,
        table_id=TABLE_NAME,
        table_resource={
            "schema": {
                "fields": [
                    {"name": "id_news", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "date_reference", "type": "DATETIME", "mode": "REQUIRED"},
                    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
                    {"name": "url", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "author", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "source", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "official_title", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "real_content", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "scrapping_status", "type": "BOOL", "mode": "REQUIRED"},
                ],
            },
        },
    )
    def bq_to_df_pipeline():
        #@task()
        #def extract_last_timestamp():
        #    hook = BigQueryHook(gcp_conn_id="gcp_conn", use_legacy_sql=False, location="US")
        #    query = f"""
        #        SELECT MAX(date_reference) as max_date
        #        FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}`
        #    """
        #    df = hook.run_query(query)
        #    max_date = df['max_date'].values[0]
        #    return max_date
        

        @task()
        def extract_bq_data():
            query = create_bq_retrieve_data_query("2023-10-01")
            hook = BigQueryHook(gcp_conn_id="gcp_conn", use_legacy_sql=False, location="US")
            df = hook.get_pandas_df(query)
             # Pour debug
            return df.to_json(orient="records",index=False)  # Pour transmettre à une autre tâche si besoin

        @task()
        def data_model(data_json):
            final_news_info = []
            my_data_loaded = json.loads(data_json)
            for news in my_data_loaded:
                url = 'https://fakenews-83331409518.europe-west9.run.app/predict'
                data = {
                    "text": news['real_content']
                }
                predicted_value = requests.post(url, json=data).json()
                news['prediction'] = mapping_score(predicted_value['score'])
                news['score'] = predicted_value['score']

                final_news_info.append(news)
                return T
        
        #max_date = extract_last_timestamp()
        my_data = extract_bq_data()
        data_model(my_data)


    dag_instance = bq_to_df_pipeline()
    create_dataset >> create_table >> dag_instance