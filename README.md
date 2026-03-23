# Portal UNACH - Sistema de Accesos Inteligentes

El **Portal UNACH** es una plataforma centralizada (HUB) desarrollada en Python con el framework Flask, diseñada para proveer a los estudiantes y funcionarios de la Universidad Adventista de Chile un punto de acceso único, rápido y seguro a todos sus servicios institucionales críticos.

## Características Principales

*   **Segmentación por Rol y Dominio:** El portal evalúa una combinación de selección de usuario y verificación de correo:
    *   Pantalla interactiva de 3 perfiles (Alumnos, Docentes, Funcionarios) previa a la solicitud de correo.
    *   `@unach.cl`: Asigna el perfil **Docente** o **Funcionario** basándose en la elección del usuario.
    *   `@alu.unach.cl`: Perfil **Alumno** (acceso a notas, intranet estudiantil, UMAS estudiantes).
    *   Correos de otros dominios son rechazados con "Acceso restringido".
*   **Clasificación Flexible y Visual:**
    *   Nueva sección visual y categoría dedicada exclusivamente a herramientas para "Docentes".
    *   Soporte para múltiples categorías por enlace (ej. un mismo servicio puede configurarse para ser visible a Docentes y Funcionarios al mismo tiempo).
*   **Personalización Dinámica:**
    *   **Saludos Sensibles al Tiempo:** El sistema detecta la hora local ("Buenos días", "Buenas tardes", "Buenas noches").
    *   **Mensajes por Rol:** Los alumnos y los funcionarios reciben textos de bienvenida, instrucciones y colores de acento distintos.
    *   **Procesamiento de Email:** Toma nombres como `juan.perez@alu.unach.cl` y los formatea a "Juan Perez" en la interfaz.
*   **Experiencia de Usuario (UX/UI):**
    *   **Tooltips Descriptivos:** Cada botón de servicio muestra una descripción contextual al pasar el cursor.
    *   **Sección de Tutoriales:** Acceso directo a videotutoriales de YouTube para Umas, Sacint, Correo Institucional y Office.
    *   **Contacto de Soporte:** Botones que abren Gmail directamente en el navegador con el correo del destinatario, asunto y nombre de usuario precargados.
    *   **Agrupación Dinámica:** Los enlaces se clasifican en 3 secciones: Servicios Principales, Tutoriales y Contacto de Soporte.
    *   **Buscador en Tiempo Real:** Permite buscar un servicio escribiendo su nombre (ej. "SIGAE").
    *   **Modo Oscuro (Dark Mode):** Alternador de tema persistente gestionado mediante `localStorage`.
    *   Diseño limpio usando Bootstrap 5 y Bootstrap Icons.
*   **Panel de Administración (Backend CRUD):**
    *   Usuarios designados en `.env` obtienen permisos de administrador.
    *   El administrador puede agregar, editar, categorizar y eliminar enlaces desde `/admin`, incluyendo la descripción para el tooltip.
    *   **Sistema de Doble Verificación:** Autenticación en dos pasos para acceder al panel admin.
*   **Seguridad Refinada:**
    *   Las sesiones caducan automáticamente luego de 60 minutos.
    *   Bloqueos de acceso directo a URL protegidas como `/dashboard` o `/admin`.


---

## Tecnologías Utilizadas
*   **Backend:** Python 3.x, Flask
*   **Base de Datos:** SQLite, gestionada mediante ORM Flask-SQLAlchemy
*   **Frontend:** HTML5, CSS3, JavaScript Vanilla, Bootstrap 5
*   **Gestión de Variables:** python-dotenv
*   **Iconos:** Bootstrap Icons

---

## Instalación y Configuración Local

Sigue estos pasos para desplegar el proyecto en un entorno de pruebas:

1. **Clonar el proyecto:**
    ```bash
    git clone https://github.com/j-alexander-acosta/Portal.UNACH.git
    cd Portal.UNACH
    ```

2. **Crear y activar un entorno virtual (Recomendado):**
    ```bash
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # En Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Variables de Entorno (`.env`):**
    Crea un archivo llamado `.env` en la raíz del proyecto y completa tus variabes secretas. (Nunca subas este archivo a repositorios públicos).
    ```env
    FLASK_SECRET_KEY=tu_clave_secreta_aleatoria
    ADMIN_EMAILS=administrador@unach.cl,otro_admin@unach.cl
    ADMIN_PASSWORD=contraseña_fuerte_de_admin
    ```

5. **Inicializar la Base de Datos:**
    Ejecuta el script para construir la base de datos SQLite pre-poblada con los enlaces básicos de la universidad:
    ```bash
    python seed_db.py
    ```

6. **Arrancar el Servidor:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000/`.

---

## Estructura del Proyecto

*   `app.py`: Núcleo de la aplicación Flask (rutas, lógica de sesión, controles de acceso).
*   `models.py`: Definición de las clases/tablas de Base de Datos para SQLAlchemy.
*   `seed_db.py`: Script autoejecutable para rellenar la base de datos con los datos iniciales obligatorios.
*   `requirements.txt`: Lista de librerías para instalación a través de pip.
*   `/templates`: 
    *   `login.html`: Pantalla de inicio de sesión dividida en 2 pasos de validación.
    *   `dashboard.html`: Vista de conectividad o tarjetero principal de la plataforma.
    *   `admin.html`: Panel CRUD para control maestro de la base de datos de los iconos.
*   `/static/styles.css`: Modificaciones de color corporativas (Azul Institucional) y manejo del tema oscuro.
