# restaurant-web-with-chatbot

Bienvenido al repositorio del Restaurante Virtual. Este proyecto es una web para un restaurante donde puedes ver el menú, obtener información general y hablar con un chatbot especializado en el restaurante.

## Características

- **Menú del Restaurante**: Consulta el menú completo del restaurante con todos los platos disponibles.
- **Información General**: Obtén información sobre los horarios de apertura, la ubicación y otros detalles importantes del restaurante.
- **Chatbot Especializado**: Interactúa con un chatbot que puede responder a tus preguntas sobre el restaurante utilizando la información proporcionada.

## Tecnologías Utilizadas

- **FastAPI**: Framework web para construir la API del chatbot.
- **OpenAI API**: Utilizada para generar respuestas del chatbot.
- **Pydantic**: Para la validación de datos.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.

## Instalación

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

## Endpoints

- **`GET /menu`**: Obtén el menú del restaurante.
- **`GET /info`**: Obtén información general sobre el restaurante.
- **`POST /chat`**: Interactúa con el chatbot enviando una pregunta en el siguiente formato:
    ```json
    {
        "question": "Dame el menú"
    }
    ```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.