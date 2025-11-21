# Despliegue del Agente de Ventas en Twilio WhatsApp

Esta guía te llevará paso a paso para conectar tu agente de ventas con WhatsApp a través de Twilio.

## 📋 Requisitos Previos

1. **Cuenta de Twilio**
   - Crea una cuenta en [Twilio](https://www.twilio.com/try-twilio)
   - Activa WhatsApp Sandbox o solicita un número de WhatsApp Business

2. **Servidor con IP pública**
   - Opciones recomendadas:
     - Railway.app (gratis para empezar)
     - Render.com (gratis para empezar)
     - Heroku
     - VPS (DigitalOcean, AWS EC2, etc.)
   - O usar ngrok para pruebas locales

3. **Variables de entorno configuradas**
   - `GOOGLE_API_KEY`: Tu clave de API de Google Gemini
   - `PORT`: Puerto para el webhook (por defecto 5000)

## 🚀 Configuración Paso a Paso

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crea o actualiza tu archivo `.env`:

```env
GOOGLE_API_KEY=tu_clave_de_google_gemini
PORT=5000
```

### 3. Iniciar el API Backend

En una terminal, inicia el backend de FastAPI:

```bash
# Primero, pobla la base de datos con productos (solo primera vez)
python -m app.seed

# Luego inicia el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

El API debe estar corriendo en `http://localhost:8000`

### 4. Iniciar el Webhook de Twilio

En otra terminal, inicia el servidor Flask:

```bash
python twilio_webhook.py
```

El webhook estará escuchando en `http://localhost:5000/webhook`

### 5. Exponer el Webhook a Internet

#### Opción A: Usando ngrok (para pruebas locales)

1. Descarga e instala [ngrok](https://ngrok.com/)
2. Ejecuta:
   ```bash
   ngrok http 5000
   ```
3. Copia la URL HTTPS que te proporciona (ejemplo: `https://abc123.ngrok.io`)

#### Opción B: Desplegar en Railway.app

1. Crea una cuenta en [Railway.app](https://railway.app/)
2. Instala Railway CLI o usa la interfaz web
3. Crea un nuevo proyecto
4. Conecta tu repositorio de GitHub
5. Configura las variables de entorno en Railway:
   - `GOOGLE_API_KEY`
   - `PORT` (Railway lo asigna automáticamente)
6. Railway te dará una URL pública

#### Opción C: Desplegar en Render.com

1. Crea una cuenta en [Render.com](https://render.com/)
2. Crea un nuevo "Web Service"
3. Conecta tu repositorio
4. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python twilio_webhook.py`
5. Añade variables de entorno
6. Render te proporcionará una URL

### 6. Configurar Twilio WhatsApp

1. Ve a la [Consola de Twilio](https://console.twilio.com/)
2. Navega a **Messaging** → **Try it out** → **Send a WhatsApp message**
3. En la sección de WhatsApp Sandbox:
   - Configura el webhook URL: `https://tu-url.com/webhook`
   - Método: `POST`
4. Guarda los cambios

Para WhatsApp Sandbox:
- Sigue las instrucciones para unirte al sandbox (enviar un código a un número)
- Envía el mensaje de activación desde tu WhatsApp

### 7. Probar el Agente

1. Abre WhatsApp en tu teléfono
2. Envía un mensaje al número del sandbox de Twilio
3. Prueba conversaciones como:
   - "Hola, ¿qué productos tienen?"
   - "Muéstrame información del producto 1"
   - "Quiero comprar 2 unidades del producto 1"
   - "Actualiza mi carrito, quiero 3 en vez de 2"

## 🏗️ Arquitectura del Sistema

```
Usuario WhatsApp
    ↓
Twilio WhatsApp API
    ↓
twilio_webhook.py (Flask)
    ↓
agent.py (LangChain + Gemini)
    ↓
app/main.py (FastAPI Backend)
    ↓
Base de Datos SQLite
```

## 📝 Estructura de Archivos

- `twilio_webhook.py`: Servidor Flask que recibe mensajes de WhatsApp
- `agent.py`: Lógica del agente con herramientas y procesamiento
- `app/session_manager.py`: Gestiona sesiones de chat por número de teléfono
- `app/main.py`: API REST de productos y carritos

## 🔧 Configuración Avanzada

### Desplegar Ambos Servicios (API + Webhook)

Si despliegas en producción, necesitas ambos servicios corriendo:

1. **Servidor de API (FastAPI)**: Puerto 8000
2. **Servidor de Webhook (Flask)**: Puerto 5000

Puedes usar un `Procfile` para servicios como Heroku:

```
web: python twilio_webhook.py
api: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

O crear un script de inicio que ejecute ambos:

```python
# start.py
import subprocess
import sys

# Inicia FastAPI en background
api_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])

# Inicia Flask webhook
subprocess.call([sys.executable, "twilio_webhook.py"])
```

### Variables de Entorno en Producción

Asegúrate de configurar:
- `GOOGLE_API_KEY`: Tu API key de Gemini
- `PORT`: Puerto para el webhook (lo asigna tu hosting)
- `API_URL`: Si despliegas el API por separado, actualiza esta variable en `agent.py`

### Usar WhatsApp Business Number

Para un número propio de WhatsApp (no sandbox):

1. En Twilio Console: **Messaging** → **Senders** → **WhatsApp senders**
2. Solicita un número de WhatsApp Business
3. Completa el proceso de verificación de Facebook Business
4. Configura el webhook en el número aprobado

## 🐛 Troubleshooting

### El agente no responde
- Verifica que ambos servicios (API y webhook) estén corriendo
- Revisa los logs del servidor Flask
- Confirma que la URL del webhook en Twilio sea correcta y accesible

### Error de API Key
- Verifica que `GOOGLE_API_KEY` esté configurada correctamente
- Asegúrate de que la API de Gemini esté habilitada en tu cuenta de Google Cloud

### Timeout en las respuestas
- El agente puede tardar en procesar mensajes complejos
- Twilio tiene un timeout de ~10 segundos para webhooks
- Considera implementar respuestas asíncronas si es necesario

### Sesiones no persisten
- El `SessionManager` usa memoria (se reinicia con el servidor)
- Para producción, considera usar Redis o una base de datos

## 🔐 Seguridad

1. **Nunca expongas tu API key** en el código
2. Usa HTTPS para todas las comunicaciones
3. Valida los requests de Twilio usando firma de seguridad:

```python
from twilio.request_validator import RequestValidator

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    # Validar firma de Twilio
    validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))
    signature = request.headers.get('X-Twilio-Signature', '')
    url = request.url
    params = request.form
    
    if not validator.validate(url, params, signature):
        return 'Forbidden', 403
    # ... resto del código
```

## 📊 Monitoreo

- Usa los logs de Twilio para ver entregas de mensajes
- Monitorea errores en tu servidor
- Considera añadir logging más detallado en producción

## 💡 Próximos Pasos

- Implementar persistencia de sesiones con Redis
- Añadir análisis de sentimiento
- Integrar pagos a través de WhatsApp
- Crear dashboard de métricas
- Implementar respuestas con multimedia (imágenes de productos)

## 📞 Recursos

- [Documentación de Twilio WhatsApp](https://www.twilio.com/docs/whatsapp)
- [Guía de Webhooks de Twilio](https://www.twilio.com/docs/usage/webhooks)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
