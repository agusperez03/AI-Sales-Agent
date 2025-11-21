# Despliegue del Agente de Ventas en Twilio WhatsApp

*Como interactuar con el numero de prueba:*

- Ingresar a chat de whatsapp con el numero: +14155238886
- Enviarle el mensaje "join meant-dirty"

Listo! El agente responderá tus mensajes, pueden comenzar con: "Hola! que productos vendes?"

Consideraciones:

- Puede buscar y recomendar productos del catalogo, crear y modificar carritos a partir de la intencion del usuario. Como notarán se va incrementando el ID del carrito y esto es porque se están almacenando, el problema es que el agente no tiene creado un acceso GET para devolverlos, por lo que me quedó visible unicamente desde un endpoint que utilicé en pruebas