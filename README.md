# 🍽️ SmartRestaurantAI | AI-Powered Restaurant Assistant  

Bienvenido a **SmartRestaurantAI**, un sistema inteligente para la gestión de pedidos y atención al cliente en restaurantes. Este proyecto permite a los usuarios interactuar con un **chatbot basado en IA** para consultar información sobre el restaurante, ver el menú y realizar pedidos, los cuales son gestionados por el equipo del restaurante en una aplicación interna.  

---

## 🚀 **Características principales**  

### 🛍️ **Para los clientes**  
✅ Consulta el **menú completo** y detalles sobre cada plato.  
✅ Pregunta información sobre el **restaurante, horarios y ubicación**.  
✅ Realiza pedidos directamente a través del **chatbot con IA**.  
✅ Confirmación del pedido y almacenamiento en la **base de datos**.  

### 🏢 **Para el restaurante**  
✅ Sistema de gestión donde los **camareros pueden aceptar o rechazar pedidos**, proporcionando una explicación.  
✅ Base de datos con registro de todos los pedidos y su estado.  

---

## 🛠️ **Tecnologías utilizadas**  

| Backend  | IA & Procesamiento  | Base de Datos | Infraestructura  |  
|----------|---------------------|--------------|----------------|  
| **FastAPI**  | **LangChain & LangGraph**  | **PostgreSQL** | **Docker & Docker Compose** |  
| **SQLAlchemy & Alembic**  | **OpenAI API (Chatbot)**  | **SQLAlchemy ORM** |  |  

---


## 📂 **Instalación y ejecución**  

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu-usuario/restaurante-virtual.git
    cd restaurante-virtual
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura tu clave de API de OpenAI:
    - Crea un archivo `.env` en la raíz del proyecto y añade tu clave de API:
        ```
        OPENAI_API_KEY=tu_clave_de_api
        ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    uvicorn main:app --reload
    ```

2. Abre tu navegador y ve a `http://127.0.0.1:8000` para interactuar con la web del restaurante.

## **🔗 Endpoints principales**
**GET /menu** → Obtiene el menú del restaurante.
**GET /info **→ Obtiene información sobre el restaurante.
**POST /chat** → Enviar una pregunta al chatbot.

    ```json
    {
        "question": "Dame el menú"
    }
    ```
**POST /order** → Realizar un pedido.
**GET /orders **→ Consultar pedidos en espera de aceptación.

--- 
## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.
