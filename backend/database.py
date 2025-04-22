
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payer_name = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.id} by {self.payer_name} at {self.timestamp}>'
