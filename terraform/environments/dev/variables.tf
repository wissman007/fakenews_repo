variable "backend" {
  description = "Backend configuration for Terraform state management"
  type        = string
  default     = "local" # Options: local, gcs
}

variable "credentials_file" {
  description = "Path to the GCP credentials file"
  type        = string
  default     = "secrets/nlpfakenews-bd7d40d4f54f.json"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "eu-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
  #default     = ""
}

variable "bucket-nlpfakenews-terraform-state" {
  description = "GCS bucket for Terraform state"
  type        = string
  default     = "bucket-nlpfakenews-terraform-state-dev"
}



variable "prefix" {
  description = "Prefix for the Terraform state files"
  type        = string
  default     = "terraform/state"
}

variable "bucket-nlp-fakenews-model-storage" {
  description = "The name of the Google Cloud Storage bucket for storing NLP model artifacts"
  type        = string
    default     = "bucket-nlp-fakenews-model-storage-dev"
}

variable "instance_airflow_image" {
  description = "The image to use for the Airflow VM instance boot disk"
  type        = string
  default     = "europe-west1-docker.pkg.dev/nlpfakenews/fake-news-repos/airflow-airflow:1.0.2"
}

variable "airflow_vm_image" {
  description = "The image to use for the Airflow VM instance boot disk"
  type        = string
}

variable "airflow_vm_tags" {
  description = "Tags to be applied to the Airflow VM instance"
  type        = list(string)
  default     = []
}

variable "airflow_vm_boot_disk_image" {
  description = "The boot disk image for the Airflow VM"
  type        = string
  default     = "debian-cloud/debian-11" # Replace with your desired image
}

variable "airflow_instance_name" {
  description = "The name of the Airflow instance"
  type        = string
  default     = "airflow-instance"
}

variable "airflow_vm_machine_type" {
  description = "Machine type for the VM instance"
  type        = string
  default     = "e2-standard-4"
}
variable "airflow_vm_network_interface" {
  description = "The network interface for the Airflow VM"
  type        = string
  default     = "default"
}

variable "tags" {
  description = "Tags to be applied to the resources"
  type        = map(string)
  default     = {
    Environment = "dev"
    Project     = "NLP-FakeNews"
  }   

 
  
}

variable "bigquery_fakenews_dataset_id" { 
    description = "The ID of the BigQuery dataset."
    type        = string
    default     = "nlpfakenews_dataset"
  }

variable "bigquery_fakenews_user_email" {
    description = "The ID of the BigQuery dataset."
    type        = string
    default     = "wissem.abdeljaouad@adventium.fr"
}
