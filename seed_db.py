import os
from app import app
from models import db, ServiceLink

# Datos iniciales (el antiguo diccionario)
LINKS_DB = {
    'comunes': [
        {'name': 'Correo', 'url': 'https://mail.google.com/', 'icon': 'bi-envelope-fill', 'description': 'Revisa tu correo institucional Gmail'},
        {'name': 'Sacint', 'url': 'https://sacint.unach.cl/', 'icon': 'bi-globe', 'description': 'Sistema Administrativo de Control y Gestión'},
        {'name': 'Biblioteca', 'url': 'https://biblioteca.unach.cl/', 'icon': 'bi-book-half', 'description': 'Acceso a la biblioteca digital y física'},
        {'name': 'SIGAE', 'url': 'https://sigae.unach.cl/login?next=/', 'icon': 'bi-hdd-network-fill', 'description': 'Sistema Integrado de Gestión Institucional'},
        {'name': 'UNACH', 'url': 'https://www.unach.cl/', 'icon': 'bi-building', 'description': 'Sitio web principal de la universidad'}
    ],
    'alumnos': [
        {'name': 'U+ Alumnos', 'url': 'https://umas-alumnos.unach.cl/Login', 'icon': 'bi-mortarboard-fill', 'description': 'Gestión de asignaturas y notas'},
        {'name': 'U+ Matrícula', 'url': 'https://umas-mnp.unach.cl/', 'icon': 'bi-card-checklist', 'description': 'Proceso de matrícula en línea'}
    ],
    'funcionarios': [
        {'name': 'U+ Docentes', 'url': 'https://umas-docentes.unach.cl/login', 'icon': 'bi-person-video3', 'description': 'Portal para ingreso de notas y asistencia'},
        {'name': 'U+ Directores', 'url': 'https://umas-bo.unach.cl/wf_desktop.aspx', 'icon': 'bi-briefcase-fill', 'description': 'Herramientas de gestión directiva'},
        {'name': 'Ciclos de Calidad', 'url': 'https://ciclos.unach.app/sign-in', 'icon': 'bi-award-fill', 'description': 'Sistema de evaluación de calidad'}
    ],
    'tutoriales': [
        {'name': 'Umas I', 'url': 'https://www.unach.cl/umas/', 'icon': 'bi-play-circle-fill', 'description': 'Tutorial básico de Umas I'},
        {'name': 'Umas II', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkZhQwsy8vgwj5amW3O3GMxj', 'icon': 'bi-play-circle-fill', 'description': 'Lista de reproducción Umas II'},
        {'name': 'Sacint', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkYPJmiMXYHTuTEEpncSVDJq', 'icon': 'bi-play-circle-fill', 'description': 'Video tutoriales de Sacint'},
        {'name': 'Correo institucional', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkb5v3yiXxOM0-v_GQr8oxpP', 'icon': 'bi-play-circle-fill', 'description': 'Configuración y uso de Correo'},
        {'name': 'Office', 'url': 'https://www.youtube.com/watch?v=y0zsn78Xx3I&list=PLWUVYuUeIWkYSm468XxFUkCBDSL1xKkxT&index=3', 'icon': 'bi-play-circle-fill', 'description': 'Tutoriales de herramientas Office'}
    ]
}

def seed():
    with app.app_context():
        # Limpiar base de links actual
        ServiceLink.query.delete()
        
        # Insertar links base
        order_idx = 0
        for category, links in LINKS_DB.items():
            # Determine section based on category name
            target_section = 'tutorial' if category == 'tutoriales' else 'main'
                
            # For these auxiliary categories, make them visible to everyone
            target_category = 'comunes' if category == 'tutoriales' else category
            
            for link_data in links:
                new_link = ServiceLink(
                    name=link_data['name'],
                    url=link_data['url'],
                    icon=link_data['icon'],
                    description=link_data.get('description', ''),
                    category=target_category,
                    section=target_section,
                    order=order_idx
                )
                db.session.add(new_link)
                order_idx += 10
                
        db.session.commit()
        print("Base de datos de enlaces inicializada correctamente.")

if __name__ == '__main__':
    seed()
