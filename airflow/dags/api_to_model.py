import datetime
import sys
import os
import time
import requests
import json
from time import sleep
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

def create_bq_retrieve_data_query(max_date):
    if max_date is None:
        query = f"""
            SELECT * 
            FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME_DATA_TO_MODEL}`
            where official_title != "cannot extract data"
            limit 1
        """
    else:
        query = f"""
            SELECT * 
            FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME_DATA_TO_MODEL}`
            where official_title != "cannot extract data" and date_reference > '{max_date}'
            limit 2
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

@task()
def extract_last_timestamp():
    hook = BigQueryHook(gcp_conn_id="gcp_conn", use_legacy_sql=False, location="US")
    query = f"""
        SELECT MAX(date_reference) as max_date
        FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}`
    """
    max_date_request = hook.get_records(query)
    if max_date_request == [[None]]:
        max_date = None
    else:
        max_date = max_date_request[0][0]
    return max_date

@task()
def extract_bq_data(max_date):
    query = create_bq_retrieve_data_query(max_date)
    hook = BigQueryHook(gcp_conn_id="gcp_conn", use_legacy_sql=False, location="US")
    df = hook.get_pandas_df(query)
    if df.empty:
        print("⚠️ Aucun résultat retourné par la requête.")
        raise Exception("Aucun résultat trouvé dans BigQuery.")
        # Tu peux gérer le cas ici : log, skip une étape, renvoyer une valeur par défaut, etc.
    else:
        print("✅ Données récupérées :", df.shape)
        # Continue le traitement ici
    df['date_reference'] = df['date_reference'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df.to_json(orient="records",index=False)

@task()
def insert_data_wrapper(query):
    insert_data_into_bigquery(query)

@task()
def data_model(data_json):
    final_news_info = []
    my_data_loaded = json.loads(data_json)
    for news in my_data_loaded:
        url = 'https://fakenews-83331409518.europe-west9.run.app/predict'
        #my_data = news['real_content'].replace('"', "'").replace("“", "'")
        my_data = news['real_content'].replace("“", " ").replace('"', ' ').replace("'", " ")

        data = {
            "text": my_data
        }
        try:
            time.sleep(2)
            value_request = requests.post(url, json=data)
            predicted_value = value_request.json()
            news['prediction'] = mapping_score(predicted_value['score'])
            news['score'] = predicted_value['score']
            news['real_content']= news['real_content'].replace("“", " ").replace('"', ' ').replace("'", " ").replace("’", " ")
            news['title'] = news['title'].replace('"', ' ').replace("'", " ").replace("“", " ").replace("’", " ")
            news['official_title'] = news['official_title'].replace('"', '').replace("'", " ").replace("“", " ").replace("’", " ")
            news['title'] = news['title'].replace('"', ' ').replace("'", " ").replace("“", " ").replace("’", " ")
            print("This is the news: ")
            print(news)
            final_news_info.append(news)
            #catch requests.exceptions.JSONDecodeError:
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            print(value_request.text)
    print(f"VOICI MA LISTE : {final_news_info}")
    return final_news_info
@task()
def generate_insert_query(data):
    query = f"""
    INSERT INTO `nlpfakenews.fake_news_detection.predicted_news` 
    (id_news, date_reference, title, url, author, source, official_title, real_content, scrapping_status, prediction, score)
    VALUES
    """
    
    values = []
    for row in data:
        print("THIS IS THE ROW FOR QUESRY : ")
        print(row)
        values.append(f"""
        ('{row['id_news']}', '{row['date_reference']}', '{row['title']}', '{row['url']}', '{row['author']}',
        '{row['source']}', '{row['official_title']}', '{row['real_content']}', {row['scrapping_status']}, 
        '{row['prediction']}', {row['score']})
        """)
    
    query += ", ".join(values)
    print(f"VOICI MA QUERY : {query}")
    return query

def insert_data_into_bigquery(query):
    insert_job = BigQueryInsertJobOperator(
        task_id='insert_data_to_bq',
        configuration={
            "query": {
                "query": query,
                "useLegacySql": False,                    }
        },  # Utiliser SQL standard BigQuery
        gcp_conn_id="gcp_conn",  # Assurez-vous que votre connexion Google Cloud est correctement configurée
    )
    return insert_job

with DAG(
    dag_id="model_to_bq",
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
                    {"name": "prediction", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "score", "type": "FLOAT", "mode": "REQUIRED"},
                ],
            },
        },
    )
        
    max_date = extract_last_timestamp()
    my_data = extract_bq_data(max_date)
    fin_data = data_model(my_data)
    query = generate_insert_query(fin_data)
    insert_task = insert_data_into_bigquery(query)


    create_dataset >> create_table >> max_date >> my_data >> fin_data >> query >> insert_task 

    