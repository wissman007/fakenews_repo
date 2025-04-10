variable "backend" {
  description = "Backend configuration for Terraform state management"
  type        = string
  default     = "local" # Options: local, gcs

}
variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "nlpfakenews"
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
variable "instance_name" {
  description = "Name of the VM instance"
  type        = string
  default     = "my-instance"
}
variable "machine_type" {
  description = "Machine type for the VM instance"
  type        = string
  default     = "n1-standard-1"
}

variable "gcs_bucket_model_storage_name" {
  description = "Name of the GCS bucket for storing NLP model artifacts"
  type        = string
  default     = "nlp-fakenews-model-storage"

}