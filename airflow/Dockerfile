FROM apache/airflow:2.10.5

USER airflow
COPY requirements_docker.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt