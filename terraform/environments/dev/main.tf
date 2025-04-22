

# add the aireflow module
module "airflow" {
  source = "../../modules/airflow"
  airflow_instance_name = var.airflow_instance_name
  airflow_vm_machine_type = var.airflow_vm_machine_type
  project_id = var.project_id
  region = var.region
  zone = var.zone
  airflow_vm_image = var.airflow_vm_image
  airflow_vm_tags = var.airflow_vm_tags
  airflow_vm_boot_disk_image = var.airflow_vm_boot_disk_image
  

 }


module "buckets" {
  source = "../../modules/storage/bucket"

  buckets = {
    "bucket-nlp-fakenews-model-storage" = {
      name     = var.bucket-nlp-fakenews-model-storage
      location = var.region
      storage_class = "STANDARD"
      versioning_enabled = true
      lifecycle_rule = [
        {
          action = {
            type = "Delete"
          }
          condition = {
            age = 30
          }
        }
      ]
    }
    "bucket-nlpfakenews-terraform-state" = {
      name     = var.bucket-nlpfakenews-terraform-state
      location = var.region
      storage_class = "STANDARD"
      versioning_enabled = true
      lifecycle_rule = [
        {
          action = {
            type = "Delete"
          }
          condition = {
            age = 30
          }
        }
      ]
    }
  }
}

module "firewall" {
  source = "../../modules/vpc/firewall"

  
}

module "dataset" {
  source = "../../modules/database/bigquery"
  project_id = var.project_id
  region = var.region
  user_email = var.bigquery_fakenews_user_email
  environment = var.environment
  dataset_id = var.bigquery_fakenews_dataset_id

}
