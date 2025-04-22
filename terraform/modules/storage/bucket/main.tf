# This Terraform configuration file sets up a Google Cloud Storage bucket for storing NLP model artifacts.

resource "google_storage_bucket" "bucket-nlpfakenews-terraform-state" {
  name          = var.buckets["bucket-nlpfakenews-terraform-state"].name
  location      = var.location
  storage_class = var.storage_class
  lifecycle {
    prevent_destroy = true
  }
  versioning {
    enabled = true
  }
 
}

resource "google_storage_bucket" "bucket-nlp-fakenews-model-storage" {
  name          = var.buckets["bucket-nlp-fakenews-model-storage"].name
  location      = var.location
  storage_class = var.storage_class
  lifecycle {
    prevent_destroy = true
  }
  versioning {
    enabled = true
  }
}