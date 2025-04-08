# This Terraform configuration file sets up a Google Cloud Storage bucket for storing NLP model artifacts.
resource "google_storage_bucket" "fake_news_model_storage" {
  name          = var.gcs_bucket_model_storage_name
  location      = "EU"
  storage_class = "STANDARD"

}



resource "google_compute_instance" "airflow_vm" {
  name         = "airflow-instance"
  machine_type = "e2-medium"
  zone         = "europe-west1-b"
  project      = var.project_id
  tags         = ["airflow"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {} # Assigns a public IP
  }

 

   metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker

    # Authenticate Docker with Artifact Registry
    gcloud auth configure-docker europe-west1-docker.pkg.dev --quiet

    mkdir -p /opt/airflow
    cd /opt/airflow

    cat <<EOF > docker-compose.yaml
    version: '3'
    services:
      postgres:
        image: postgres:13
        restart: always
        environment:
          POSTGRES_USER: airflow
          POSTGRES_PASSWORD: airflow
          POSTGRES_DB: airflow

      redis:
        image: redis:alpine
        restart: always

      webserver:
        image: europe-west1-docker.pkg.dev/nlpfakenews/fake-news-repos/airflow-airflow:latest
        depends_on:
          - postgres
          - redis
        ports:
          - "8080:8080"
        environment:
          AIRFLOW__CORE__EXECUTOR: CeleryExecutor
          AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
          AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres:5432/airflow
          AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
          AIRFLOW__CORE__LOGGING_LEVEL: INFO
          AIRFLOW__LOGGING__LOGGING_LEVEL: INFO
          AIRFLOW__LOGGING__BASE_LOG_FOLDER: /opt/airflow/logs
          AIRFLOW__LOGGING__REMOTE_LOGGING: "False"

          AIRFLOW_UID: 1001
          DATASET_NAME: fake_news_detection_terraform
          TABLE_NAME: training_data_v2
          CLIENT_ID: mV7cQmIvF_HI_f4rdB7qUQ
          SECRET_KEY: mc8t6uX8xsdp_F67vzUdV1mzb8ElCA
          MY_PROJECT: nlpfakenews
          AIRFLOW__WEBSERVER__WORKERS: 4

        
        command: webserver
       

      scheduler:
        image: europe-west1-docker.pkg.dev/nlpfakenews/fake-news-repos/airflow-airflow:latest
        depends_on:
          - webserver
        environment:
          AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
          AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
          AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres:5432/airflow
          AIRFLOW__CORE__LOGGING_LEVEL: INFO
          AIRFLOW__LOGGING__LOGGING_LEVEL: INFO
          AIRFLOW__LOGGING__BASE_LOG_FOLDER: /opt/airflow/logs
          AIRFLOW__LOGGING__REMOTE_LOGGING: "False"

          AIRFLOW_UID: 1001
          DATASET_NAME: fake_news_detection_terraform
          TABLE_NAME: training_data_v2
          CLIENT_ID: mV7cQmIvF_HI_f4rdB7qUQ
          SECRET_KEY: mc8t6uX8xsdp_F67vzUdV1mzb8ElCA
          MY_PROJECT: nlpfakenews

        command: scheduler
      
      api-service:
        image: europe-west1-docker.pkg.dev/nlpfakenews/fake-news-repos/api:0.5.0
        restart: always
        ports:
          - "5000:5000"
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
          interval: 30s
          timeout: 10s
          retries: 5


    EOF

    sudo docker-compose up -d
  EOT

  metadata = {
    "google-compute-default-credentials" = "true"
  }

  service_account {
    email  = "fakenews-gcr@nlpfakenews.iam.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
  labels = {
    env = "dev"
  }
}