

variable "project_id" {
  description = "The project ID"
  type        = string
}

variable "region" {
  description = "The region for the resources"
  type        = string
  default     = "europe-west1"
}
variable "zone" {
  description = "The zone for the resources"
  type        = string
  default     = "europe-west1-b"
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


variable "airflow_vm_network_interface" {
  description = "The network interface for the Airflow VM"
  type        = string
  default     = "default"
}
