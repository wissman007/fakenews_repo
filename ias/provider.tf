terraform {
required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.28.0"
    }
  }
  backend "local" {
    path = "${path.module}/terraform.tfstate"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
