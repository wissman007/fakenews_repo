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
    sudo apt install -y python3-pip git
    sudo systemctl start docker
    sudo systemctl enable docker


    mkdir -p /opt/airflow/
    cd /opt/airflow/

    # Create a Docker Compose file
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
        healthcheck:
          test: ["CMD", "pg_isready", "-U", "airflow"]
          interval: 5s
          retries: 5
          start_period: 10s

      git-sync:
        image: k8s.gcr.io/git-sync:v3.1.6
        restart: always
        user: "0:0" # Run as root

        environment:
          GIT_SYNC_REPO: "https://abdeljaouad.wissem%40gmail.com:z%26ZD%25W30%q@github.com/HadjMohamed/NLP-FakeNews.git"
          GIT_SYNC_BRANCH: "dev"
          GIT_SYNC_WAIT: "30"
          GIT_SYNC_DEST: "repo"
          GIT_SYNC_ROOT: "/dags"
          GIT_SYNC_ONE_TIME: "true" 
          GIT_SYNC_DEPTH: "1"
            

        volumes:
          - /opt/dags/mount:/dags 

      airflow-init:
        image: apache/airflow:2.6.0-python3.10
        restart: on-failure
        depends_on:
          postgres:
            condition: service_healthy
        environment:
          AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
        command: ["airflow", "db", "init"]   
      
      webserver:
        image: apache/airflow:2.6.0-python3.10
        restart: always
        user: "0:0" # Run as root
        depends_on:
          - postgres
          - airflow-init
          - git-sync
        environment:
          AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
          AIRFLOW__WEBSERVER__RBAC: "True"
          AIRFLOW_WWW_USER_CREATE: "true"
          AIRFLOW_WWW_USER_USERNAME: "admin"
          AIRFLOW_WWW_USER_PASSWORD: "admin"
          AIRFLOW_WWW_USER_FIRSTNAME: "Wissem"
          AIRFLOW_WWW_USER_LASTNAME: "Abdeljaouad"
          AIRFLOW_WWW_USER_EMAIL: "wissem@example.com"
          AIRFLOW_WWW_USER_ROLE: "Admin"
        ports:
          - "8080:8080"
        volumes:
          - /opt/dags/mount/repo/airflow/dags:/opt/airflow/dags
          - /opt/dags/mount/repo/airflow:/opt/airflow/src
          

        command: >
            bash -c " airflow users create --username admin --firstname Wissem --lastname Abdeljaouad --role Admin --email abdeljaouad.wissem@gmail.com --password admin 
            && su - airflow -c 'pip install --user -r /opt/airflow/src/requirements_docker.txt' 
            && airflow webserver"

      scheduler:
        image: apache/airflow:2.6.0-python3.10
        restart: always
        depends_on:
          - webserver
        environment:
          AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
        command: ["scheduler"]
        volumes:
          - /opt/dags/mount/repo/airflow/dags:/opt/airflow/dags

    EOF

    # Start Airflow
    sudo docker-compose up -d
  EOT
}