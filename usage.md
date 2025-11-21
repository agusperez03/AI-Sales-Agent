# Guía de Uso

Esta guía explica cómo levantar el entorno y utilizar el agente de ventas.

## Prerrequisitos

- Python 3.13 (ya configurado en `venv`)
- Clave de API de Google Gemini

## Configuración

1.  **Activar entorno virtual**:
    ```powershell
    .\venv\Scripts\activate
    ```

2.  **Instalar dependencias** (si no se ha hecho):
    ```powershell
    pip install -r requirements.txt
    ```

3.  **Configurar variables de entorno**:
    -   Abre el archivo `.env`.
    -   Coloca tu `GOOGLE_API_KEY`.

4.  **Inicializar Base de Datos**:
    -   Asegúrate de que `products.xlsx` esté en la raíz (o se usarán datos de prueba).
    -   Ejecuta el script de seed:
    ```powershell
    python -m app.seed
    ```

## Ejecución

Necesitarás dos terminales.

### Terminal 1: API Backend

Levanta el servidor de la API:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.
Puedes ver la documentación interactiva en `http://127.0.0.1:8000/docs`.

### Terminal 2: Agente IA

Ejecuta el agente de consola:

```powershell
python agent.py
```

## Ejemplo de Interacción

```text
User: Hola, ¿qué vendes?
Agent: Hola! En Laburen.com tenemos los siguientes productos disponibles:
- Laptop: High performance laptop ($999.99)
- Mouse: Wireless mouse ($29.99)
- Keyboard: Mechanical keyboard ($89.99)

User: Quiero una laptop y un teclado.
Agent: ¡Excelente elección! He creado un carrito para ti con los siguientes productos:
- 1x Laptop
- 1x Keyboard
Tu ID de carrito es 1.

User: Agrega un mouse también.
Agent: He actualizado tu carrito (ID 1). Ahora incluye:
- 1x Laptop
- 1x Keyboard
- 1x Mouse
```
