
# Frontend (Vue.js con Vite)

Este directorio contiene la interfaz de usuario para la aplicación Coffee Tracker.

## Setup

1.  **Asegúrate de tener Node.js y npm instalados.** Puedes descargarlos desde [https://nodejs.org/](https://nodejs.org/).

2.  **Navega a este directorio:**
    ```bash
    cd frontend
    ```

3.  **Instala las dependencias:**
    ```bash
    npm install
    ```

4.  **IMPORTANTE: Edita `src/App.vue`:**
    *   Busca las líneas `const friend1 = "YOUR_NAME"` y `const friend2 = "FRIEND_NAME"`.
    *   Reemplaza `"YOUR_NAME"` y `"FRIEND_NAME"` con vuestros nombres reales. ¡Estos deben coincidir *exactamente* con los nombres configurados en el backend (`app.py`)!
    *   Verifica la línea `const apiUrl = 'http://localhost:5000/api'`. Si ejecutas el backend en una máquina o puerto diferente, ajusta esta URL.

## Ejecución (Modo Desarrollo)

1.  **Inicia el servidor de desarrollo de Vite:**
    ```bash
    npm run dev
    ```
    Esto compilará la aplicación y la servirá localmente. Abre tu navegador en la dirección que indique (normalmente `http://localhost:5173`).

## Build (Para Producción)

1.  **Genera los archivos estáticos para desplegar:**
    ```bash
    npm run build
    ```
    Los archivos resultantes estarán en la carpeta `dist/`. Estos archivos se pueden servir desde cualquier servidor web estático.
