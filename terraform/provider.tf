terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend remoto en S3 
  backend "s3" {
    bucket         = "iac-tf-bucket-s3"
    key            = "ecs-demo/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}
#aws configure indican aws secret id y aws secret key
# export AWS_ACCESS_KEY_ID="your_access_key_id"
# export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
#aws get-caller-identity para verificar que las credenciales son correctas