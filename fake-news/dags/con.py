import datetime
import os
import time
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from pprint import pprint
from airflow.decorators import task
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateTableOperator, BigQueryInsertJobOperator, BigQueryCreateEmptyDatasetOperator, BigQueryUpsertTableOperator

DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")

create_dataset = BigQueryCreateEmptyDatasetOperator(task_id="create_dataset", dataset_id=DATASET_NAME)

upsert_table = BigQueryUpsertTableOperator(
    gcp_conn_id= "gcp_co",
    task_id="upsert_table",
    dataset_id=os.getenv("DATASET_NAME"),
    table_resource={
        "tableReference": {"tableId": "test_table_id"},
    },
)

create_table = BigQueryCreateTableOperator(
    gcp_conn_id= "gcp_co",
    task_id="create_table",
    dataset_id=DATASET_NAME,
    table_id=TABLE_NAME,
    table_resource={
        "schema": {
            "fields": [
                {"name": "id_news", "type": "STRING", "mode": "REQUIRED"},
                {"name": "title", "type": "STRING", "mode": "NULLABLE"},
                {"name": "content", "type": "STRING", "mode": "REQUIRED"},
                {"name": "source", "type": "STRING", "mode": "REQUIRED"},
                {"name": "flag", "type": "INTEGER", "mode": "REQUIRED"},
            ],
        },
    },
)
#delete_doublon = BigQueryInsertJobOperator(
#    task_id="insert_query_job",
#    query = 
#    configuration={
#        "query": {
#            "query": INSERT_ROWS_QUERY,
#            "useLegacySql": False,
#            "priority": "BATCH",
#        }
#    },
#)

@task(task_id="print_the_context")
def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"

run_this = print_context()

with DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily",
):
    EmptyOperator(task_id="task") >> run_this >> create_table