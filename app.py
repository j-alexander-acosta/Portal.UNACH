import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, ServiceLink
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super_secret_key_unach_portal')
app.permanent_session_lifetime = timedelta(minutes=60)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'profile' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Por favor ingrese su correo.', 'warning')
            return redirect(url_for('login'))
        
        # Check if Admin
        admin_emails = os.environ.get('ADMIN_EMAILS', '').split(',')
        is_admin = email in admin_emails
        
        if is_admin:
            password = request.form.get('password')
            if password is None:
                # Ask for password step
                return render_template('login.html', require_password=True, email=email)
            
            admin_password = os.environ.get('ADMIN_PASSWORD', '')
            if password != admin_password:
                flash('Contraseña de administrador incorrecta.', 'danger')
                return render_template('login.html', require_password=True, email=email)
            
            session.permanent = True
            session['profile'] = 'Admin'
            session['email'] = email
            return redirect(url_for('dashboard'))
        elif email.endswith('@unach.cl'):
            session.permanent = True
            session['profile'] = 'Funcionario'
            session['email'] = email
            return redirect(url_for('dashboard'))
        elif email.endswith('@alu.unach.cl'):
            session.permanent = True
            session['profile'] = 'Alumno'
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Acceso restringido a cuentas institucionales UNACH', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'profile' not in session:
        return redirect(url_for('login'))
    
    profile = session['profile']
    
    # Calculate time-based greeting
    from datetime import datetime
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        greeting = "Buenos días"
    elif 12 <= current_hour < 19:
        greeting = "Buenas tardes"
    else:
        greeting = "Buenas noches"
    
    # Query database for active links
    common_links = ServiceLink.query.filter_by(category='comunes', is_active=True).all()
    
    profile_links = []
    if profile == 'Alumno':
        profile_links = ServiceLink.query.filter_by(category='alumnos', is_active=True).all()
    elif profile in ['Funcionario', 'Admin']:
        profile_links = ServiceLink.query.filter_by(category='funcionarios', is_active=True).all()
        
    all_links = sorted(common_links + profile_links, key=lambda x: x.order)
    
    # Extract username from email
    email = session.get('email', '')
    username = email.split('@')[0] if email else 'Usuario'
    user_data = {'username': username}
        
    return render_template('dashboard.html', 
                         profile=profile, 
                         email=email, 
                         links=all_links, 
                         greeting=greeting,
                         user=user_data)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- ADMIN ROUTES ---

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('profile') != 'Admin':
            flash('Acceso denegado: Se requiere perfil de Administrador.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    links = ServiceLink.query.order_by(ServiceLink.order).all()
    return render_template('admin.html', links=links, email=session.get('email'))

@app.route('/admin/link/add', methods=['POST'])
@admin_required
def admin_link_add():
    name = request.form.get('name')
    url = request.form.get('url')
    icon = request.form.get('icon')
    description = request.form.get('description')
    category = request.form.get('category')
    section = request.form.get('section', 'main')
    order = request.form.get('order', type=int, default=0)
    
    new_link = ServiceLink(name=name, url=url, icon=icon, description=description, category=category, section=section, order=order)
    db.session.add(new_link)
    db.session.commit()
    flash('Enlace agregado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/delete/<int:link_id>', methods=['POST'])
@admin_required
def admin_link_delete(link_id):
    link = ServiceLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Enlace eliminado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/toggle/<int:link_id>', methods=['POST'])
@admin_required
def admin_link_toggle(link_id):
    link = ServiceLink.query.get_or_404(link_id)
    link.is_active = not link.is_active
    db.session.commit()
    flash(f"Enlace '{link.name}' {'activado' if link.is_active else 'desactivado'}.", 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/edit/<int:link_id>', methods=['POST'])
@admin_required
def admin_link_edit(link_id):
    link = ServiceLink.query.get_or_404(link_id)
    link.name = request.form.get('name')
    link.url = request.form.get('url')
    link.icon = request.form.get('icon')
    link.category = request.form.get('category')
    link.section = request.form.get('section', 'main')
    link.order = request.form.get('order', type=int, default=0)
    
    db.session.commit()
    flash('Enlace editado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
