# Terraform variables for the development environment on GCP



# Environment name
environment = "dev"

# Project ID
project_id = "nlpfakenews"
# Credentials file path
credentials_file = "secrets/nlpfakenews-bd7d40d4f54f.json"

# Backend configuration
backend = "gcs" # Options: local, gcs
bucket-nlpfakenews-terraform-state = "bucket-nlpfakenews-terraform-state-dev"
prefix = "terraform/state"
region = "europe-west1"


#path = "${path.module}/terraform.tfstate"

# Airflow VM configuration
airflow_instance_name = "airflow-instance-dev"
airflow_vm_image = "europe-west1-docker.pkg.dev/nlpfakenews/fake-news-repos/airflow-airflow:1.0.2"
airflow_vm_machine_type = "e2-medium"
airflow_vm_tags = ["airflow"]
airflow_vm_boot_disk_image = "ubuntu-os-cloud/ubuntu-2204-lts"
airflow_vm_network_interface = "default"

# S3 bucket configuration model storage
bucket-nlp-fakenews-model-storage = "bucket-nlp-fakenews-model-storage-dev"

# datasert configuration
bigquery_fakenews_dataset_id = "fakenews_dataset_dev"
bigquery_fakenews_user_email = "wissem.abdeljaouad@adventium.Fr"

# Tags
tags = {
    Environment = "dev"
    Project     = "NLP-FakeNews"
}