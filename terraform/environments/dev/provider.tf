terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.28.0"
    }
  }
  # This backend configuration is for storing Terraform state in Google Cloud Storage (GCS).
  # The bucket name and prefix are specified for the GCS backend.
  backend "gcs" {
    bucket = "bucket_nlpfakenews_terraform_state-dev"
    prefix = "terraform/state"

  }
}
# This provider block configures the Google Cloud provider for Terraform.
# It specifies the project, region, and credentials file to use for authentication.
provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}