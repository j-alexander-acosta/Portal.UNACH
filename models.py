import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ServiceLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False) # 'comunes', 'alumnos', 'funcionarios'
    section = db.Column(db.String(50), default='main') # 'main', 'tutorial', 'support'
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ServiceLink {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_type = db.Column(db.String(20), nullable=False) # 'Alumno' o 'Funcionario'
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

class GlobalAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), default='info') # 'info', 'warning', 'danger', 'success'
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<GlobalAlert {self.id}>'
