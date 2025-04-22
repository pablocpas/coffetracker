
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .database import db, Payment # Use relative import
import os
from datetime import datetime # Asegúrate de importar datetime si no lo hiciste en database.py

# --- Configuración ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True) # Asegura que el directorio 'instance' exista
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "coffee.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicialización ---
db.init_app(app)
CORS(app) # Habilita CORS para todas las rutas (ajusta en producción si es necesario)

# --- Creación de la tabla (solo la primera vez o si no existe) ---
with app.app_context():
    db.create_all()

# --- Nombres de los amigos (¡¡IMPORTANTE!! Edita estos valores) ---
# Asegúrate de que estos nombres coinciden EXACTAMENTE con los del frontend.
FRIEND1_NAME = "CAÑO"  # <-- CAMBIA ESTO
FRIEND2_NAME = "BARRIO" # <-- CAMBIA ESTO

# --- Rutas de la API (prefijo /api) ---
@app.route('/api/last_payer', methods=['GET'])
def get_last_payer():
    """Devuelve el nombre de la última persona que pagó y el contador total."""
    last_payment = Payment.query.order_by(Payment.timestamp.desc()).first()
    count = Payment.query.count()
    if last_payment:
        return jsonify({"last_payer": last_payment.payer_name, "count": count})
    else:
        # Nadie ha pagado aún, estado inicial "equilibrado"
        return jsonify({"last_payer": None, "count": 0})

@app.route('/api/pay', methods=['POST'])
def record_payment():
    """Registra un nuevo pago."""
    data = request.get_json()
    payer = data.get('payer_name')

    if not payer or payer not in [FRIEND1_NAME, FRIEND2_NAME]:
        app.logger.warning(f"Intento de pago inválido recibido: {data}")
        app.logger.warning(f"Intento de pago inválido recibido: {data}")
        return jsonify({"error": f"Nombre de pagador inválido o faltante. Recibido: '{payer}'. Esperado: '{FRIEND1_NAME}' o '{FRIEND2_NAME}'"}), 400

    new_payment = Payment(payer_name=payer)
    db.session.add(new_payment)
    db.session.commit()
    count = Payment.query.count() # Obtener el nuevo contador

    app.logger.info(f"Nuevo pago registrado: {payer}") # Log para consola
    # Devolver también el nuevo contador
    return jsonify({"success": True, "payer_name": payer, "count": count}), 201

# (Opcional) Ruta para ver historial
@app.route('/api/history', methods=['GET'])
def get_history():
    """Devuelve el historial de pagos ordenado por fecha."""
    payments = Payment.query.order_by(Payment.timestamp.desc()).all()
    history = [{"payer": p.payer_name, "time": p.timestamp.isoformat()} for p in payments]
    return jsonify(history)

@app.route('/api/reset', methods=['DELETE'])
def reset_payments():
    """Borra todo el historial de pagos."""
    try:
        num_deleted = db.session.query(Payment).delete()
        db.session.commit()
        app.logger.info(f"Historial de pagos reseteado. {num_deleted} registros eliminados.")
        # Devolvemos el estado reseteado (sin pagador, contador 0)
        return jsonify({"success": True, "message": "Historial reseteado.", "last_payer": None, "count": 0}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al resetear el historial: {e}")
        return jsonify({"error": "Error interno al intentar resetear el historial."}), 500


# --- Rutas para servir el frontend estático ---
# Sirve el archivo principal index.html
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    dist_path = os.path.join(os.path.dirname(__file__), 'dist')
    if path != "" and os.path.exists(os.path.join(dist_path, path)):
        # Sirve archivos específicos (JS, CSS, imágenes, etc.)
        return send_from_directory(dist_path, path)
    else:
        # Sirve index.html para cualquier otra ruta (manejo de SPA)
        return send_from_directory(dist_path, 'index.html')

# --- Ejecución ---
if __name__ == '__main__':
    # Escucha en todas las IPs locales, útil para acceder desde otro dispositivo en la red
    # debug=True es útil para desarrollo, pero desactívalo en producción
    app.run(host='0.0.0.0', port=5000, debug=True)
