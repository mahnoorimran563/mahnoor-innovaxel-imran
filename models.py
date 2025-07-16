from datetime import datetime
from extensions import db  


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    shortCode = db.Column(db.String(10), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    accessCount = db.Column(db.Integer, default=0)
