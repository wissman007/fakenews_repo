# Terraform variables for the development environment on GCP

# GCP region
gcp_region = "us-central1"

# Environment name
environment = "dev"

# Project ID
project_id = "my-dev-project"
# Credentials file path
credentials_file = "path/to/credentials.json"

path = "${path.module}/terraform.tfstate"


# VPC configuration
vpc_cidr = "10.0.0.0/16"

# Subnet configuration
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]

# Instance configuration
instance_type = "t2.micro"
key_name = "dev-key"

# RDS configuration
rds_instance_class = "db.t3.micro"
rds_engine = "postgres"
rds_username = "admin"
rds_password = "securepassword"



# S3 bucket configuration
s3_bucket_name = "dev-fake-news-bucket"

# Tags
tags = {
    Environment = "dev"
    Project     = "NLP-FakeNews"
}