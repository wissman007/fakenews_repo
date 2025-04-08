import datetime
import sys
import os
import time
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from pprint import pprint
from airflow.decorators import task
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateTableOperator, BigQueryInsertJobOperator, BigQueryCreateEmptyDatasetOperator, BigQueryUpsertTableOperator
sys.path.append("/opt/airflow")
from scripts.main import main

DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
#PROJECT_NAME = os.get("PROJECT_NAME")
PROJECT_NAME="nlpfakenews"

def create_bq_delete_query(ti):
    # Récupère la valeur depuis XCom
    result1, resultat2 = ti.xcom_pull(task_ids='call_external_function') 
    #resultat2 = ['1jqdoke', '1jqdjsw', '1jqdj5f', '1jqdido', '1jqdhq9', '1jqdg5s', '1jqdat4']
    # Crée la requête SQL en utilisant les résultats récupérés
    query = f"""
        DELETE FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}`
        WHERE id_news IN UNNEST({resultat2})
    """
    return query
def insert_data_query(ti):
    df, result2 = ti.xcom_pull(task_ids='call_external_function')
    # Convertir le DataFrame en une liste de dictionnaires (format adapté pour la requête SQL)
    rows = df.to_dict(orient="records")

    # Générer dynamiquement les noms des colonnes et les valeurs dans la requête SQL
    columns = ', '.join(df.columns)  # Créer la liste des colonnes
    values = ', '.join([f"({', '.join([repr(item[col]) for col in df.columns])})" for item in rows])  # Générer les valeurs pour chaque ligne

    # Préparer la requête d'insertion
    query = f"""
    INSERT INTO `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}` ({columns})
    VALUES
    {values}
    """
    return query

with DAG(
    dag_id="scrapping_inserting_news",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
):
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
    create_query_delete_rows = PythonOperator(
        task_id="create_bq_delete_query",
        python_callable=create_bq_delete_query,
        provide_context=True  # Nécessaire pour accéder à ti
    )

    create_query_insert_rows = PythonOperator(
        task_id="insert_data_query",
        python_callable=insert_data_query,
        provide_context=True  # Nécessaire pour accéder à ti
    )
    create_dataset = BigQueryCreateEmptyDatasetOperator(gcp_conn_id= "gcp_conn",task_id="create_dataset", dataset_id=DATASET_NAME)
    scrapping_data = PythonOperator(
        task_id="call_external_function",
        python_callable=main  # Appelle la fonction
    )
    delete_row = BigQueryInsertJobOperator(
    gcp_conn_id= "gcp_conn",
    task_id="delete_rows",
    configuration={
        "query": {
            "query": "{{ task_instance.xcom_pull(task_ids='create_bq_delete_query') }}",
            "useLegacySql": False,
            "priority": "BATCH",
            }
        },
    )
    insert_rows = BigQueryInsertJobOperator(
        gcp_conn_id= "gcp_conn",
        task_id="insert_rows",
        configuration={
            "query": {
                "query": "{{ task_instance.xcom_pull(task_ids='insert_data_query') }}",
                "useLegacySql": False,
                "priority": "BATCH",
            }
        },
    )
    create_dataset >> create_table >> scrapping_data >> create_query_delete_rows >> delete_row >> create_query_insert_rows >> insert_rows