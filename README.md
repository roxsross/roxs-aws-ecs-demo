# ECS Demo - Arquitectura AWS con Fargate

[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-ECS_Fargate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/ecs/)
[![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)](https://aws.amazon.com/dynamodb/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0+-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Aplicación web Python (Flask) con interfaz moderna desplegada en AWS ECS con Fargate, siguiendo las mejores prácticas de arquitectura cloud-native.

## ✨ Características

- 🎨 **Interfaz Web Moderna** - UI hermosa con HTML, CSS y JavaScript
- 🚀 **Flask Framework** - Backend Python ligero y potente
- 📊 **Dashboard Interactivo** - Gestión visual de items
- 🔄 **CRUD Completo** - Crear, leer, actualizar y eliminar items
- 🎯 **API REST** - Endpoints JSON para integración
- ☁️ **AWS ECS Fargate** - Contenedores serverless
- 💾 **DynamoDB** - Base de datos NoSQL escalable
- 📈 **Auto Scaling** - Escalado automático basado en métricas
- 🔒 **Seguridad** - IAM roles, Security Groups, VPC privada

## 🏗️ Arquitectura

La aplicación implementa la siguiente arquitectura AWS:

```
Internet → ALB → ECS Fargate Tasks → DynamoDB
                      ↓
                    ECR (Container Images)
```

### Componentes

- **Application Load Balancer (ALB)**: Distribuye tráfico HTTP/HTTPS
- **Amazon ECS con Fargate**: Ejecuta contenedores sin gestionar servidores
- **Amazon ECR**: Registro de imágenes Docker
- **Amazon DynamoDB**: Base de datos NoSQL serverless
- **CloudWatch**: Logs y métricas
- **IAM**: Roles y políticas de seguridad
- **VPC**: Red privada con subnets públicas y privadas

## 📋 Requisitos Previos

- AWS CLI configurado con credenciales
- Docker instalado
- Terraform >= 1.0
- Python 3.11+ (para desarrollo local)
- jq (para scripts de testing)

## 🚀 Ejecución Local

### Opción 1: Docker Compose (Recomendado)

La forma más rápida de ejecutar el proyecto localmente es usando Docker Compose, que incluye DynamoDB Local:

```bash
# 1. Clonar el repositorio
git clone https://github.com/roxsross/roxs-aws-ecs-demo.git
cd roxs-aws-ecs-demo

# 2. Construir y levantar los contenedores
docker-compose up --build -d

# 3. Crear la tabla en DynamoDB Local
aws dynamodb create-table \
  --table-name local-table \
  --attribute-definitions \
    AttributeName=id,AttributeType=S \
  --key-schema \
    AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# 4. Verificar que la tabla fue creada
aws dynamodb list-tables \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# 5. Acceder a la aplicación
# Abrir en el navegador: http://localhost:8080
```

La aplicación estará disponible en `http://localhost:8080` y usará una instancia local de DynamoDB.

**Comandos útiles:**

```bash
# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Detener los servicios
docker-compose down

# Reconstruir las imágenes
docker-compose up --build --force-recreate
```

### Opción 2: Entorno Virtual Python

Para desarrollo con recarga automática:

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux

# 2. Instalar dependencias
cd app
pip install -r requirements.txt

# 3. Configurar variables de entorno
export DYNAMODB_TABLE=local-table
export AWS_REGION=us-east-1
export ENVIRONMENT=local
export PORT=8080
export DYNAMODB_ENDPOINT=http://localhost:8000

# 4. Iniciar DynamoDB Local en otro terminal
docker run -p 8000:8000 amazon/dynamodb-local:latest \
  -jar DynamoDBLocal.jar -sharedDb -inMemory

# 5. Crear la tabla en DynamoDB Local (en otro terminal)
aws dynamodb create-table \
  --table-name local-table \
  --attribute-definitions \
    AttributeName=id,AttributeType=S \
  --key-schema \
    AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# 6. Ejecutar la aplicación
python main.py

# La aplicación estará en http://localhost:8080
```

### Opción 3: Solo Docker

```bash
# 1. Construir la imagen
docker build -t ecs-demo-app .

# 2. Ejecutar DynamoDB Local
docker run -d --name dynamodb-local -p 8000:8000 \
  amazon/dynamodb-local:latest

# 3. Crear la tabla en DynamoDB Local
aws dynamodb create-table \
  --table-name local-table \
  --attribute-definitions \
    AttributeName=id,AttributeType=S \
  --key-schema \
    AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# 4. Ejecutar la aplicación
docker run -d \
  --name ecs-demo-app \
  -p 8080:8080 \
  -e AWS_REGION=us-east-1 \
  -e DYNAMODB_TABLE=local-table \
  -e ENVIRONMENT=local \
  -e DYNAMODB_ENDPOINT=http://dynamodb-local:8000 \
  --link dynamodb-local \
  ecs-demo-app

# 5. Acceder a la aplicación
# http://localhost:8080
```

### 🧪 Probar la Aplicación

Una vez que la aplicación esté corriendo, puedes:

**Interfaz Web:**
- Navegar a `http://localhost:8080`
- Crear, editar y eliminar items desde la UI

**API REST:**

```bash
# Health check
curl http://localhost:8080/health

# Obtener información del sistema
curl http://localhost:8080/info

# Listar items
curl http://localhost:8080/api/items

# Crear un item
curl -X POST http://localhost:8080/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Prueba desde API"}'

# Obtener un item específico
curl http://localhost:8080/api/items/<item_id>

# Actualizar un item
curl -X PUT http://localhost:8080/api/items/<item_id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "description": "Item actualizado"}'

# Eliminar un item
curl -X DELETE http://localhost:8080/api/items/<item_id>
```

### 🔍 Verificar DynamoDB Local

Puedes verificar que DynamoDB Local está corriendo:

```bash
# Listar tablas
aws dynamodb list-tables \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# Ver items en la tabla (después de crear algunos)
aws dynamodb scan \
  --table-name local-table \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

**Nota:** DynamoDB Local no requiere credenciales AWS reales, usa credenciales ficticias.

### 🗄️ Gestión de la Tabla DynamoDB Local

**Crear la tabla manualmente:**

```bash
aws dynamodb create-table \
  --table-name local-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

**Eliminar la tabla:**

```bash
aws dynamodb delete-table \
  --table-name local-table \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

**Insertar datos de prueba manualmente:**

```bash
aws dynamodb put-item \
  --table-name local-table \
  --item '{"id": {"S": "test-123"}, "name": {"S": "Item de Prueba"}, "description": {"S": "Descripción de prueba"}, "created_at": {"S": "2025-11-01T10:00:00Z"}}' \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

**Ver todos los items:**

```bash
aws dynamodb scan \
  --table-name local-table \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

###  Troubleshooting

**Error: "Cannot do operations on a non-existent table"**
```bash
# La tabla no existe, necesitas crearla primero
aws dynamodb create-table \
  --table-name local-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

**Error de conexión a DynamoDB:**
```bash
# Verificar que DynamoDB Local está corriendo
docker ps | grep dynamodb

# Ver logs de DynamoDB Local
docker logs dynamodb-local
```

**Puerto ya en uso:**
```bash
# Cambiar el puerto en docker-compose.yml
ports:
  - "8081:8080"  # Usar 8081 en lugar de 8080
```

**Problemas con permisos en macOS:**
```bash
# Dar permisos al volumen
chmod -R 755 ./app
```

## 🔧 Configuración

### Variables de Entorno

La aplicación utiliza las siguientes variables de entorno:

- `DYNAMODB_TABLE`: Nombre de la tabla DynamoDB (default: `ecs-demo-table`)
- `AWS_REGION`: Región de AWS (default: `us-east-1`)
- `ENVIRONMENT`: Ambiente de ejecución (default: `development`)
- `PORT`: Puerto de la aplicación (default: `8080`)


## 📁 Estructura del Proyecto

```
.
├── app/
│   ├── main.py              # Aplicación FastAPI
│   └── requirements.txt     # Dependencias Python
├── Dockerfile              # Imagen Docker
├── .dockerignore          # Archivos ignorados por Docker
└── README.md              # Este archivo
```


## 📚 Recursos Adicionales

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

## 📝 Licencia

MIT License

## 👥 Autor

RoxsRoss DevOps
