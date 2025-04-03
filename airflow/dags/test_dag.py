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

@task()
def create_bq_delete_query(ti):
    result1, result2 = ti.xcom_pull(task_ids='call_external_function')
    query = f"""
        DELETE FROM `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}`
        WHERE id_news IN UNNEST({result2})
    """
    return query

@task()
def insert_data_query(ti):
    df, result2 = ti.xcom_pull(task_ids='call_external_function')
    rows = df.to_dict(orient="records")
    columns = ', '.join(df.columns)
    values = ', '.join([f"({', '.join([repr(item[col]) for col in df.columns])})" for item in rows])
    query = f"""
    INSERT INTO `{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}` ({columns})
    VALUES
    {values}
    """
    return query

with DAG(
    dag_id="test_dag",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
) as dag:

    create_dataset = BigQueryCreateEmptyDatasetOperator(
        gcp_conn_id="gcp_conn",
        task_id="create_dataset",
        dataset_id=DATASET_NAME
    )
    
    create_table = BigQueryCreateTableOperator(
        gcp_conn_id="gcp_conn",
        task_id="create_table_intermediaire",
        dataset_id=DATASET_NAME,
        table_id=TABLE_NAME,
        table_resource={ ... }
    )

    scrapping_data = PythonOperator(
        task_id="call_external_function",
        python_callable=main
    )

    create_query_delete_rows = create_bq_delete_query()
    create_query_insert_rows = insert_data_query()

    delete_row = BigQueryInsertJobOperator(
        gcp_conn_id="gcp_conn",
        task_id="delete_rows",
        configuration={ "query": { "query": "{{ task_instance.xcom_pull(task_ids='create_bq_delete_query') }}", "useLegacySql": False, "priority": "BATCH" }}
    )
    
    insert_rows = BigQueryInsertJobOperator(
        gcp_conn_id="gcp_conn",
        task_id="insert_rows",
        configuration={ "query": { "query": "{{ task_instance.xcom_pull(task_ids='insert_data_query') }}", "useLegacySql": False, "priority": "BATCH" }}
    )

    # Organiser les dépendances
    create_dataset >> create_table >> scrapping_data >> create_query_delete_rows >> delete_row >> create_query_insert_rows >> insert_rows
