import os
from app import app
from models import db, ServiceLink

# Datos iniciales (el antiguo diccionario)
LINKS_DB = {
    'comunes': [
        {'name': 'Correo', 'url': 'https://mail.google.com/', 'icon': 'bi-envelope-fill'},
        {'name': 'Sacint', 'url': 'https://sacint.unach.cl/', 'icon': 'bi-globe'},
        {'name': 'Biblioteca', 'url': 'https://biblioteca.unach.cl/', 'icon': 'bi-book-half'},
        {'name': 'SIGAE', 'url': 'https://sigae.unach.cl/login?next=/', 'icon': 'bi-hdd-network-fill'},
        {'name': 'UNACH', 'url': 'https://www.unach.cl/', 'icon': 'bi-building'}
    ],
    'alumnos': [
        {'name': 'U+ Alumnos', 'url': 'https://umas-alumnos.unach.cl/Login', 'icon': 'bi-mortarboard-fill'},
        {'name': 'U+ Matrícula', 'url': 'https://umas-mnp.unach.cl/', 'icon': 'bi-card-checklist'}
    ],
    'funcionarios': [
        {'name': 'U+ Docentes', 'url': 'https://umas-docentes.unach.cl/login', 'icon': 'bi-person-video3'},
        {'name': 'U+ Directores', 'url': 'https://umas-bo.unach.cl/wf_desktop.aspx', 'icon': 'bi-briefcase-fill'},
        {'name': 'Ciclos de Calidad', 'url': 'https://ciclos.unach.app/sign-in', 'icon': 'bi-award-fill'}
    ]
}

def seed():
    with app.app_context():
        # Limpiar base de links actual
        ServiceLink.query.delete()
        
        # Insertar links base
        order_idx = 0
        for category, links in LINKS_DB.items():
            for link_data in links:
                new_link = ServiceLink(
                    name=link_data['name'],
                    url=link_data['url'],
                    icon=link_data['icon'],
                    category=category,
                    order=order_idx
                )
                db.session.add(new_link)
                order_idx += 10
                
        db.session.commit()
        print("Base de datos de enlaces inicializada correctamente.")

if __name__ == '__main__':
    seed()
