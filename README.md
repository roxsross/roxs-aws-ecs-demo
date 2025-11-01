# ECS Demo - Arquitectura AWS con Fargate

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
