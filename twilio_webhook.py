from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from app.session_manager import session_manager
from agent import process_message
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)

SYSTEM_MESSAGE = "You are a helpful sales assistant for Laburen.com. You can list products, show details, and manage shopping carts. Always verify product availability before adding to cart. When a user wants to buy, create a cart for them. If they want to change something, update the cart."

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook endpoint for Twilio WhatsApp messages."""
    
    print("=" * 50)
    print("📩 WEBHOOK RECIBIDO")
    print("=" * 50)
    
    # Get incoming message details
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    print(f"Mensaje: {incoming_msg}")
    print(f"De: {from_number}")
    print(f"Todos los datos: {dict(request.values)}")
    
    # Create Twilio response
    resp = MessagingResponse()
    
    if not incoming_msg:
        resp.message("Por favor envía un mensaje.")
        return str(resp)
    
    try:
        # Get or initialize session
        print(f"🔍 Obteniendo sesión para {from_number}...")
        chat_history = session_manager.get_session(from_number)
        
        # If new session, add system message
        if not chat_history:
            print("✨ Nueva sesión creada")
            chat_history = [("system", SYSTEM_MESSAGE)]
        else:
            print(f"📚 Sesión existente con {len(chat_history)} mensajes")
        
        # Add user message to history
        chat_history.append(("user", incoming_msg))
        
        # Process message with agent
        print("🤖 Procesando mensaje con el agente...")
        agent_response, updated_history = process_message(incoming_msg, chat_history)
        print(f"✅ Respuesta del agente: {agent_response[:100]}...")
        
        # Update session with new history
        session_manager.update_session(from_number, updated_history)
        
        # Send response back to user
        resp.message(agent_response)
        print("📤 Respuesta enviada")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(traceback.format_exc())
        resp.message("Lo siento, hubo un error procesando tu mensaje. Por favor intenta de nuevo.")
    
    return str(resp)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Twilio WhatsApp webhook is running"}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Iniciando servidor Flask en puerto {port}...")
    print(f"📍 Webhook URL: http://0.0.0.0:{port}/webhook")
    print(f"💚 Health check: http://0.0.0.0:{port}/health")
    app.run(host='0.0.0.0', port=port, debug=True)
