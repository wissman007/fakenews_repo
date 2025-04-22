# This file contains the variable definitions for the BigQuery dataset module.
variable "project_id" {
  description = "The ID of the GCP project."
  type        = string
}
variable "region" {
  description = "The region where the BigQuery dataset will be created."
  type        = string
  default     = "europe-west1"
}
variable "user_email" {
  description = "The email of the user who will have access to the dataset."
  type        = string
    
}

variable "environment" {
  description = "The environment for the dataset (e.g., dev, prod)."
  type        = string
  default     = "dev"
}
variable "dataset_id" {
  
}