import os
import sqlite3
from app import app
from models import db, ServiceLink

SUPPORT_LINKS = [
    {'name': 'Correos', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=soporte.correos@unach.cl', 'icon': 'bi-envelope', 'email': 'soporte.correos@unach.cl'},
    {'name': 'U+', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=soporte.umas@unach.cl', 'icon': 'bi-mortarboard', 'email': 'soporte.umas@unach.cl'},
    {'name': 'Sacint', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=soporte.sacint@unach.cl', 'icon': 'bi-globe', 'email': 'soporte.sacint@unach.cl'},
    {'name': 'Campus Virtual', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=jefevirtualunach@unach.cl', 'icon': 'bi-laptop', 'email': 'jefevirtualunach@unach.cl'},
    {'name': 'Biblioteca', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=soporteinformatico@unach.cl', 'icon': 'bi-book', 'email': 'soporteinformatico@unach.cl'},
    {'name': 'DAIE', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to=informaticodaie@unach.cl', 'icon': 'bi-info-circle', 'email': 'informaticodaie@unach.cl'}
]

def migrate():
    # 1. Add column via raw SQLite since SQLAlchemy doesn't easily do it without Alembic
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'portal.db')
    
    print(f"Connecting to DB at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists first
        cursor.execute("PRAGMA table_info(service_link)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'section' not in columns:
            print("Adding 'section' column to service_link table...")
            cursor.execute("ALTER TABLE service_link ADD COLUMN section VARCHAR(50) DEFAULT 'main'")
        else:
            print("Column 'section' already exists. Skipping ALTER TABLE.")
            
        conn.commit()
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        conn.close()
        
    # 2. Update existing links and insert Support links using SQLAlchemy
    with app.app_context():
        # Update existing tutorial links to section='tutorial'
        tutorial_links = ServiceLink.query.filter(ServiceLink.name.like('%Tutoriales%')).all()
        for link in tutorial_links:
            link.section = 'tutorial'
            print(f"Updated {link.name} to section='tutorial'")
            
        # Insert or update Support Links
        order_idx = 0
        for data in SUPPORT_LINKS:
            existing = ServiceLink.query.filter_by(name=data['name'], section='support').first()
            if not existing:
                new_link = ServiceLink(
                    name=data['name'],
                    url=data['url'],
                    icon=data['icon'],
                    category='comunes', # Visible to all
                    section='support',
                    order=order_idx
                )
                db.session.add(new_link)
                print(f"Inserted support link: {data['name']}")
            else:
                print(f"Support link {data['name']} already exists. Skipping.")
            order_idx += 10
            
        db.session.commit()
        print("Migration complete!")

if __name__ == '__main__':
    migrate()
