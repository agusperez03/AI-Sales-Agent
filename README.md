# Laburen Challenge - AI Sales Agent

- **CODIGO Y DOCUMENTACIÓN ACTUALIZADO EN LA RAMA "TWILIO"**


Este proyecto implementa un agente de IA capaz de vender productos mediante una API REST y una base de datos.

## Estructura

- `app/`: Código fuente del Backend (API).
- `docs/`: Documentación de arquitectura y uso.
- `agent.py`: Script del agente de IA (Cliente).
- `products.xlsx`: Fuente de datos de productos.

## Inicio Rápido

Consulta [docs/usage.md](docs/usage.md) para instrucciones detalladas.

1.  Configura `.env` con tu `GOOGLE_API_KEY`.
2.  Instala dependencias: `pip install -r requirements.txt`.
3.  Carga datos: `python -m app.seed`.
4.  Inicia API: `uvicorn app.main:app --reload`.
5.  Inicia Agente: `python agent.py`.
