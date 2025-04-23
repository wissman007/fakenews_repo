# add big query resource
resource "google_bigquery_dataset" "fakenews_dataset" {
  dataset_id = var.dataset_id
  location   = var.region
  project    = var.project_id

    labels = {
        environment = var.environment
    }
  
}