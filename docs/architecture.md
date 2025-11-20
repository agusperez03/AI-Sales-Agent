# Arquitectura del Agente de Ventas Laburen

## Diagrama de Flujo

```mermaid
sequenceDiagram
    participant User as Usuario
    participant Agent as Agente IA (Gemini)
    participant API as API REST (FastAPI)
    participant DB as Base de Datos (PostgreSQL/SQLite)

    User->>Agent: "Hola, quiero ver qué productos tienen"
    Agent->>API: GET /products
    API->>DB: Query Products
    DB-->>API: List[Products]
    API-->>Agent: JSON Products
    Agent-->>User: "Tenemos Laptop, Mouse, Keyboard..."

    User->>Agent: "Quiero comprar una Laptop y 2 Mouse"
    Agent->>API: POST /carts {items: [{id:1, qty:1}, {id:2, qty:2}]}
    API->>DB: Insert Cart & Items
    DB-->>API: Cart Created
    API-->>Agent: JSON Cart
    Agent-->>User: "Listo, he creado tu carrito con ID 1. ¿Necesitas algo más?"

    User->>Agent: "Mejor quita un Mouse"
    Agent->>API: PATCH /carts/1 {items: [{id:2, qty:1}]}
    API->>DB: Update Cart Item
    DB-->>API: Cart Updated
    API-->>Agent: JSON Cart
    Agent-->>User: "Actualizado. Ahora tienes 1 Mouse."
```

## Componentes

1.  **Agente IA (Cliente)**:
    -   Implementado en Python usando `langgraph` y `langchain-google-genai`.
    -   Utiliza el modelo **Gemini 2.5 Flash**.
    -   Interactúa con el usuario vía consola (fase actual).
    -   Consume la API REST mediante llamadas HTTP (Tools).

2.  **API REST (Backend)**:
    -   Framework: **FastAPI**.
    -   Endpoints para gestión de productos y carritos.
    -   Documentación automática en `/docs`.

3.  **Base de Datos**:
    -   **SQLite** para desarrollo local (fácil despliegue).
    -   Compatible con **PostgreSQL** mediante cambio de connection string en `database.py`.
    -   ORM: **SQLAlchemy**.

4.  **Datos**:
    -   Carga inicial desde `products.xlsx` mediante script de seed.
