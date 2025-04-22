
# Backend (Flask API)

Este directorio contiene el servidor backend para la aplicación Coffee Tracker.

## Setup

1.  **Navega a este directorio:**
    ```bash
    cd backend
    ```

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **IMPORTANTE: Edita `app.py`:**
    *   Busca las líneas `FRIEND1_NAME = "YOUR_NAME"` y `FRIEND2_NAME = "FRIEND_NAME"`.
    *   Reemplaza `"YOUR_NAME"` y `"FRIEND_NAME"` con vuestros nombres reales. ¡Estos deben coincidir *exactamente* con los nombres usados en el frontend!

## Ejecución

1.  **Inicia el servidor Flask:**
    ```bash
    python app.py
    ```
    El servidor estará disponible en `http://localhost:5000` (o la IP de tu máquina en el puerto 5000). La base de datos (`coffee.db`) se creará automáticamente dentro de la carpeta `instance`.
