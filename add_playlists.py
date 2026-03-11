import os
from app import app
from models import db, ServiceLink

NEW_LINKS = [
    {'name': 'U+ Tutoriales', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkZhQwsy8vgwj5amW3O3GMxj', 'icon': 'bi-youtube'},
    {'name': 'Sacint Tutoriales', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkYPJmiMXYHTuTEEpncSVDJq', 'icon': 'bi-youtube'},
    {'name': 'Correo Inst. Tutoriales', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkb5v3yiXxOM0-v_GQr8oxpP', 'icon': 'bi-youtube'},
    {'name': 'Utilitarios Tutoriales', 'url': 'https://www.youtube.com/playlist?list=PLWUVYuUeIWkYSm468XxFUkCBDSL1xKkxT', 'icon': 'bi-youtube'}
]

def add_playlists():
    with app.app_context():
        # Get max order to append at the end
        max_order_link = ServiceLink.query.order_by(ServiceLink.order.desc()).first()
        current_order = max_order_link.order + 10 if max_order_link else 0
        
        for link_data in NEW_LINKS:
            # Check if it already exists to prevent duplicates
            existing = ServiceLink.query.filter_by(url=link_data['url']).first()
            if not existing:
                new_link = ServiceLink(
                    name=link_data['name'],
                    url=link_data['url'],
                    icon=link_data['icon'],
                    category='comunes', # Putting them in comunes so everyone sees them
                    order=current_order
                )
                db.session.add(new_link)
                current_order += 10
                print(f"Added {link_data['name']}")
            else:
                print(f"Skipped {link_data['name']} (already exists)")
                
        db.session.commit()
        print("Playlists added successfully.")

if __name__ == '__main__':
    add_playlists()
