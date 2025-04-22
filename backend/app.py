
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, Payment
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

# --- Rutas de la API ---
@app.route('/api/last_payer', methods=['GET'])
def get_last_payer():
    """Devuelve el nombre de la última persona que pagó."""
    last_payment = Payment.query.order_by(Payment.timestamp.desc()).first()
    if last_payment:
        return jsonify({"last_payer": last_payment.payer_name})
    else:
        # Nadie ha pagado aún, estado inicial "equilibrado"
        return jsonify({"last_payer": None})

@app.route('/api/pay', methods=['POST'])
def record_payment():
    """Registra un nuevo pago."""
    data = request.get_json()
    payer = data.get('payer_name')

    if not payer or payer not in [FRIEND1_NAME, FRIEND2_NAME]:
        app.logger.warning(f"Intento de pago inválido recibido: {data}")
        return jsonify({"error": f"Nombre de pagador inválido o faltante. Recibido: '{payer}'. Esperado: '{FRIEND1_NAME}' o '{FRIEND2_NAME}'"}), 400

    new_payment = Payment(payer_name=payer)
    db.session.add(new_payment)
    db.session.commit()

    app.logger.info(f"Nuevo pago registrado: {payer}") # Log para consola
    return jsonify({"success": True, "payer_name": payer}), 201

# (Opcional) Ruta para ver historial
@app.route('/api/history', methods=['GET'])
def get_history():
    """Devuelve el historial de pagos ordenado por fecha."""
    payments = Payment.query.order_by(Payment.timestamp.desc()).all()
    history = [{"payer": p.payer_name, "time": p.timestamp.isoformat()} for p in payments]
    return jsonify(history)

# --- Ejecución ---
if __name__ == '__main__':
    # Escucha en todas las IPs locales, útil para acceder desde otro dispositivo en la red
    # debug=True es útil para desarrollo, pero desactívalo en producción
    app.run(host='0.0.0.0', port=5000, debug=True)
