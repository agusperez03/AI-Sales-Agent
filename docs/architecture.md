# Arquitectura del Agente de Ventas Laburen

## Arquitectura de Alto Nivel

El sistema está compuesto por cuatro capas principales que trabajan en conjunto para ofrecer un agente de ventas conversacional a través de WhatsApp:

```
Usuario WhatsApp
       ↓
Twilio API (Servicio Externo)
       ↓
Webhook Flask (twilio_webhook.py)
       ↓
Agente IA (agent.py + LangGraph)
       ↓
API REST (FastAPI)
       ↓
Base de Datos (SQLite/PostgreSQL)
```

## Componentes Principales

### 1. **LLM (Large Language Model)**
- **Modelo**: Google Gemini 2.5 Flash
- **Framework**: LangChain + LangGraph
- **Función**: Procesa lenguaje natural, ejecuta herramientas (tools) y mantiene contexto conversacional
- **Ubicación**: `agent.py`

### 2. **Servicios Externos - WhatsApp**
- **Proveedor**: Twilio WhatsApp API
- **Función**: Canal de comunicación con usuarios finales
- **Flujo**: Twilio recibe mensajes → envía a webhook → devuelve respuestas

### 3. **Webhook Handler**
- **Framework**: Flask
- **Función**: Recibe requests HTTP de Twilio, gestiona sesiones por número de teléfono, coordina LLM y API
- **Ubicación**: `twilio_webhook.py`
- **Gestión de Sesiones**: `app/session_manager.py` (mantiene historial conversacional en memoria)

### 4. **API REST (Backend)**
- **Framework**: FastAPI
- **Endpoints**:
  - `GET /products` - Listar productos (con búsqueda opcional)
  - `GET /products/{id}` - Detalles de producto
  - `POST /carts` - Crear carrito
  - `PATCH /carts/{id}` - Actualizar carrito
- **Documentación**: Auto-generada en `/docs`
- **Ubicación**: `app/main.py`

### 5. **Base de Datos**
- **Desarrollo**: SQLite (archivo local)
- **Producción**: Compatible con PostgreSQL
- **ORM**: SQLAlchemy
- **Modelos**: `app/models.py`
- **Inicialización**: Script de seed carga productos desde `products.xlsx`
