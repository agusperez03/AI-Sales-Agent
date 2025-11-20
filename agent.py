from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
import requests
import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field

load_dotenv()

API_URL = "http://127.0.0.1:8000"

class CartItemInput(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    qty: int = Field(..., description="Quantity of the product")

@tool
def list_products(query: str = None):
    """List available products. Optional query to filter by name or description."""
    params = {"q": query} if query else {}
    try:
        response = requests.get(f"{API_URL}/products", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error fetching products: {e}"

@tool
def get_product_details(product_id: int):
    """Get details of a specific product by ID."""
    try:
        response = requests.get(f"{API_URL}/products/{product_id}")
        if response.status_code == 404:
            return "Product not found."
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error fetching product details: {e}"

@tool
def create_cart(items: List[CartItemInput]):
    """Create a new cart with items."""
    try:
        items_data = [item.model_dump() for item in items]
        response = requests.post(f"{API_URL}/carts", json={"items": items_data})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error creating cart: {e}"

@tool
def update_cart(cart_id: int, items: List[CartItemInput]):
    """Update an existing cart. Use qty=0 to remove an item."""
    try:
        items_data = [item.model_dump() for item in items]
        response = requests.patch(f"{API_URL}/carts/{cart_id}", json={"items": items_data})
        if response.status_code == 404:
            return "Cart not found."
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error updating cart: {e}"

def run_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Please set GOOGLE_API_KEY in .env file.")
        return

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0)
    tools = [list_products, get_product_details, create_cart, update_cart]
    
    system_message = "You are a helpful sales assistant for Laburen.com. You can list products, show details, and manage shopping carts. Always verify product availability before adding to cart. When a user wants to buy, create a cart for them. If they want to change something, update the cart."

    agent_executor = create_react_agent(llm, tools)

    # Initialize chat history with system message
    chat_history = [("system", system_message)]

    print("Agent is ready! Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Add user message to history
        chat_history.append(("user", user_input))
        
        try:
            # Invoke agent with full history
            response = agent_executor.invoke({"messages": chat_history})
            
            # Update history with the new state (includes tool calls and AI response)
            chat_history = response['messages']
            
            # Get the last message (AI response)
            last_message = chat_history[-1]
            content = last_message.content
            
            # Handle content if it's a list (Gemini specific)
            if isinstance(content, list):
                text_content = ""
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_content += block.get("text", "")
                print(f"Agent: {text_content}")
            else:
                print(f"Agent: {content}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_agent()
