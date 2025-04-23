# variable "gcs_bucket_model_storage_name" {
#   description = "The name of the Google Cloud Storage bucket for storing NLP model artifacts"
#   type        = string
#     default     = "nlp-fakenews-model-storage"
# }
# variable "bucket_nlpfakenews_terraform_state" {
#   description = "GCS bucket for Terraform state"
#   type        = string
#   default     = "nlpfakenews_terraform_state"
# }

variable "buckets" {
  description = "List of GCS bucket names"
  type        = map(object({
    name          = string
    location      = string
    storage_class = string
  }))
  
    default     = {
    "bucket-nlp-fakenews-model-storage" = {
      name          = "bucket-nlp-fakenews-model-storage"
      location      = "EU"
      storage_class = "STANDARD"
    }
    "bucket-nlpfakenews-terraform-state" = {
      name          = "bucket-nlpfakenews-terraform-state"
      location      = "EU"
      storage_class = "STANDARD"
    }
  }
  
}

variable "location" {
  description = "Location for the GCS bucket"
  type        = string
  default     = "EU"
}
variable "storage_class" {
  description = "Storage class for the GCS bucket"
  type        = string
  default     = "STANDARD"
  
}