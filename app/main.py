"""
Aplicación Flask para arquitectura AWS ECS
Implementa interfaz web con templates HTML y API REST
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import boto3
from botocore.exceptions import ClientError
import os
import logging
from datetime import datetime
import uuid

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Configuración de DynamoDB
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "ecs-demo-table")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", None)

# Cliente DynamoDB
if DYNAMODB_ENDPOINT:
    # Usar DynamoDB local
    dynamodb = boto3.resource('dynamodb', 
                             region_name=AWS_REGION,
                             endpoint_url=DYNAMODB_ENDPOINT)
else:
    # Usar DynamoDB en AWS
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

table = dynamodb.Table(DYNAMODB_TABLE)

# ============================================================================
# RUTAS WEB (HTML)
# ============================================================================

@app.route("/")
def index():
    """Página principal con lista de items"""
    try:
        response = table.scan()
        items = response.get('Items', [])
        # Ordenar por fecha de creación (más recientes primero)
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return render_template('index.html', items=items)
    except Exception as e:
        logger.error(f"Error loading items: {str(e)}")
        flash(f"Error al cargar items: {str(e)}", "error")
        return render_template('index.html', items=[])

@app.route("/create", methods=["GET", "POST"])
def create():
    """Crear nuevo item"""
    if request.method == "POST":
        try:
            item_id = str(uuid.uuid4())
            item_data = {
                'id': item_id,
                'name': request.form.get('name'),
                'description': request.form.get('description', ''),
                'status': request.form.get('status', 'active'),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item_data)
            logger.info(f"Item created: {item_id}")
            flash("Item creado exitosamente!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            flash(f"Error al crear item: {str(e)}", "error")
    
    return render_template('create.html')

@app.route("/edit/<item_id>", methods=["GET", "POST"])
def edit(item_id):
    """Editar item existente"""
    if request.method == "POST":
        try:
            update_expression = "SET updated_at = :updated_at"
            expression_values = {':updated_at': datetime.utcnow().isoformat()}
            expression_names = {}
            
            if request.form.get('name'):
                update_expression += ", #n = :name"
                expression_values[':name'] = request.form.get('name')
                expression_names['#n'] = 'name'
            
            if request.form.get('description') is not None:
                update_expression += ", description = :description"
                expression_values[':description'] = request.form.get('description')
            
            if request.form.get('status'):
                update_expression += ", #s = :status"
                expression_values[':status'] = request.form.get('status')
                expression_names['#s'] = 'status'
            
            table.update_item(
                Key={'id': item_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_names if expression_names else None,
                ExpressionAttributeValues=expression_values
            )
            
            logger.info(f"Item updated: {item_id}")
            flash("Item actualizado exitosamente!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            flash(f"Error al actualizar item: {str(e)}", "error")
    
    # GET request - mostrar formulario con datos actuales
    try:
        response = table.get_item(Key={'id': item_id})
        if 'Item' not in response:
            flash("Item no encontrado", "error")
            return redirect(url_for('index'))
        return render_template('edit.html', item=response['Item'])
    except Exception as e:
        logger.error(f"Error getting item: {str(e)}")
        flash(f"Error al cargar item: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route("/delete/<item_id>", methods=["POST"])
def delete(item_id):
    """Eliminar item"""
    try:
        table.delete_item(Key={'id': item_id})
        logger.info(f"Item deleted: {item_id}")
        flash("Item eliminado exitosamente!", "success")
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        flash(f"Error al eliminar item: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route("/info")
def info():
    """Página de información del sistema"""
    info_data = {
        "container_id": os.getenv("HOSTNAME", "unknown"),
        "aws_region": AWS_REGION,
        "dynamodb_table": DYNAMODB_TABLE,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat()
    }
    return render_template('info.html', info=info_data)

# ============================================================================
# API REST (JSON)
# ============================================================================

@app.route("/health")
def health_check():
    """Health check para ALB"""
    try:
        table.table_status
        return jsonify({
            "status": "healthy",
            "dynamodb": "connected",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route("/api/items", methods=["GET"])
def api_list_items():
    """API: Listar todos los items"""
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify({"count": len(items), "items": items})
    except ClientError as e:
        logger.error(f"Error listing items: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["GET"])
def api_get_item(item_id):
    """API: Obtener un item específico"""
    try:
        response = table.get_item(Key={'id': item_id})
        if 'Item' not in response:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(response['Item'])
    except ClientError as e:
        logger.error(f"Error getting item: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items", methods=["POST"])
def api_create_item():
    """API: Crear nuevo item"""
    try:
        data = request.get_json()
        item_id = data.get('id', str(uuid.uuid4()))
        item_data = {
            'id': item_id,
            'name': data.get('name'),
            'description': data.get('description', ''),
            'status': data.get('status', 'active'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=item_data)
        logger.info(f"Item created: {item_id}")
        return jsonify({"message": "Item created successfully", "item": item_data}), 201
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["PUT"])
def api_update_item(item_id):
    """API: Actualizar item"""
    try:
        data = request.get_json()
        update_expression = "SET updated_at = :updated_at"
        expression_values = {':updated_at': datetime.utcnow().isoformat()}
        expression_names = {}
        
        if data.get('name'):
            update_expression += ", #n = :name"
            expression_values[':name'] = data.get('name')
            expression_names['#n'] = 'name'
        
        if 'description' in data:
            update_expression += ", description = :description"
            expression_values[':description'] = data.get('description')
        
        if data.get('status'):
            update_expression += ", #s = :status"
            expression_values[':status'] = data.get('status')
            expression_names['#s'] = 'status'
        
        response = table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names if expression_names else None,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )
        
        logger.info(f"Item updated: {item_id}")
        return jsonify({"message": "Item updated successfully", "item": response['Attributes']})
    except Exception as e:
        logger.error(f"Error updating item: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["DELETE"])
def api_delete_item(item_id):
    """API: Eliminar item"""
    try:
        table.delete_item(Key={'id': item_id})
        logger.info(f"Item deleted: {item_id}")
        return jsonify({"message": "Item deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("ENVIRONMENT") == "development")
