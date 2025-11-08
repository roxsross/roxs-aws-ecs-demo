# ========================================
# Configuración del Proyecto
# ========================================
# Estos valores se pueden versionar en Git

project_name = "ecs-demo"
environment  = "development"

# Tags para recursos AWS
tags = {
  "Project"   = "Ecs-demo"
  "ManagedBy" = "Terraform"
  "Owner"     = "Roxs Development"
}

# ========================================
# Capacidad de Auto Scaling
# ========================================
min_capacity = 2
max_capacity = 4

# ========================================
# ⚠️ CONFIGURACIÓN DE RED (Sensible)
# ========================================
# Los valores de VPC y Subnets NO deben estar aquí.
# Se configuran vía:
#   1. GitHub Secrets (CI/CD)
#   2. Variables de entorno locales (TF_VAR_*)
#   3. terraform.tfvars.local (no versionado)
#
# Ver: terraform/README-CICD.md para más detalles
# ========================================
##
use_existing_vpc            = true
# existing_vpc_id             = "vpc-xxxxx"  # ← Configurar en GitHub Secrets
# existing_private_subnet_ids = ["subnet-xxxxx", "subnet-yyyyy"]
# existing_public_subnet_ids  = ["subnet-xxxxx"]