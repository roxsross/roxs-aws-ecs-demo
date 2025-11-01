variable "aws_region" {
  description = "Region de AWS"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  default     = "ecs-demo"
  description = "nombre del proyecto"
}

variable "environment" {
  type        = string
  default     = "development"
  description = "Ambiente (development, staging, productions)"
}

variable "tags" {
  description = "Tags para recursos de AWS"
  type        = map(string)
  default = {
    "Project"   = "Ecs-demo"
    "ManagedBy" = "Terraform"
    "Owner"     = "Roxs Development"
  }
}
#### vpc

variable "use_existing_vpc" {
  description = "Si es true, usa una VPC existente. Si es false, crea una nueva VPC"
  type        = bool
  default     = false
}

variable "existing_vpc_id" {
  description = "ID de la VPC existente (requerido si use_existing_vpc = true)"
  type        = string
  default     = ""
}

variable "existing_private_subnet_ids" {
  type        = list(string)
  default     = []
  description = "IDs de las subnets privadas"
}

variable "existing_public_subnet_ids" {
  type        = list(string)
  default     = []
  description = "IDs de las subnets públicas"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "CIDR block for the VPC"
}

variable "availability_zones" {
  description = "Zonas de disponibilidad"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "private_subnets" {
  description = "Subnets privadas"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]

}

variable "public_subnets" {
  description = "Subnets públicas"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]

}

variable "max_capacity" {
  description = "Maximum number of instances in the ECS Cluster Auto Scaling Group"
  type        = number
  default     = 3
}
variable "min_capacity" {
  description = "Minimum number of instances in the ECS Cluster Auto Scaling Group"
  type        = number
  default     = 1
}