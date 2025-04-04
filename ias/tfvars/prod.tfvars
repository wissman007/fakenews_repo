# Terraform variables for development environment on GCP

# GCP Region and Zone
gcp_region = "us-central1"
gcp_zone = "us-central1-a"

# VPC Configuration
vpc_name = "dev-vpc"
subnet_names = ["dev-subnet-1", "dev-subnet-2"]

# Compute Engine Instance Configuration
machine_type = "e2-medium"
ssh_key_name = "dev-key"

# Cloud SQL Configuration
db_tier = "db-f1-micro"
db_name = "dev_db"
db_username = "admin"
db_password = "devpassword"

# Cloud Storage Bucket Configuration
bucket_name = "dev-bucket-name"

# Application Configuration
app_environment = "development"
app_version = "1.0.0"