# Terraform variables for the development environment on GCP

# GCP region
gcp_region = "eu-west1"

# Environment name
environment = "dev"

# Project ID
project_id = "nlpfakenews"
# Credentials file path
credentials_file = "secrets/nlpfakenews-bd7d40d4f54f.json"

# Backend configuration
backend = "gcs" # Options: local, gcs
bucket_nlpfakenews_terraform_state = "nlpfakenews_terraform_state-${environment}"
prefix = "terraform/state"
region = gcp_region

#path = "${path.module}/terraform.tfstate"

# Airflow VM configuration
airflow_vm_name = "airflow-instance"
airflow_vm_machine_type = "e2-medium"
airflow_vm_zone = "europe-west1-b"
airflow_vm_tags = ["airflow"]
airflow_vm_boot_disk_image = "ubuntu-os-cloud/ubuntu-2204-lts"
airflow_vm_network = "default"
airflow_git_sync_image = "k8s.gcr.io/git-sync:v3.1.6"
airflow_git_repo = "https://github.com/HadjMohamed/NLP-FakeNews.git"

# S3 bucket configuration model storage
gcs_bucket_model_storage_name = "fake_news_model_storage-${environment}"

# Tags
tags = {
    Environment = "dev"
    Project     = "NLP-FakeNews"
}