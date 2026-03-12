import sys

def rewrite_admin():
    file_path = '/Users/alexanderacosta/Documents/Proyectos/portal.unach/templates/admin.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Macro definition replacing the single table.
    macro_start = """
        {% macro render_links_table(table_title, section_links) %}
        <h4 class="fw-bold mt-4 mb-3 text-secondary">{{ table_title }}</h4>
        <div class="card shadow-sm border-0 rounded-4 mb-4">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th class="ps-4">Categoría</th>
                                <th>Orden</th>
                                <th>Icono</th>
                                <th>Nombre</th>
                                <th>URL</th>
                                <th>Estado</th>
                                <th class="pe-4 text-end">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for link in section_links %}
"""
    
    # 2. Extract the inner part of the loop from original (lines 69 to 143)
    start_tag = "{% for link in links %}"
    end_tag = "{% endfor %}"
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag) + len(end_tag)
    
    inner_loop = content[start_idx + len(start_tag) : end_idx - len(end_tag)]
    
    # We need to add the section select in the edit modal inside inner_loop
    edit_modal_marker = '<div class="row">'
    section_select_edit = """
                                                            <div class="col-md-6 mb-3">
                                                                <label class="form-label fw-semibold">Sección</label>
                                                                <select class="form-select" name="section" required>
                                                                    <option value="main" {% if link.section == 'main' %}selected{% endif %}>Principal</option>
                                                                    <option value="tutorial" {% if link.section == 'tutorial' %}selected{% endif %}>Tutorial</option>
                                                                    <option value="support" {% if link.section == 'support' %}selected{% endif %}>Soporte</option>
                                                                </select>
                                                            </div>
"""
    
    # Let's insert the section_select right before the category select
    # The existing code has <div class="col-md-6 mb-3"> for Categoría. We will change the row to have 3 cols or just add another row.
    # It's easier to replace the <div class="row"> content.
    edit_row_replacement = """
                                                        <div class="row">
                                                            <div class="col-md-4 mb-3">
                                                                <label class="form-label fw-semibold">Sección</label>
                                                                <select class="form-select" name="section" required>
                                                                    <option value="main" {% if link.section == 'main' %}selected{% endif %}>Principal</option>
                                                                    <option value="tutorial" {% if link.section == 'tutorial' %}selected{% endif %}>Tutoriales</option>
                                                                    <option value="support" {% if link.section == 'support' %}selected{% endif %}>Soporte</option>
                                                                </select>
                                                            </div>
                                                            <div class="col-md-4 mb-3">
                                                                <label class="form-label fw-semibold">Categoría</label>
                                                                <select class="form-select" name="category" required>
                                                                    <option value="comunes" {% if link.category == 'comunes' %}selected{% endif %}>Comunes</option>
                                                                    <option value="alumnos" {% if link.category == 'alumnos' %}selected{% endif %}>Solo Alumnos</option>
                                                                    <option value="funcionarios" {% if link.category == 'funcionarios' %}selected{% endif %}>Solo Funcionarios</option>
                                                                </select>
                                                            </div>
                                                            <div class="col-md-4 mb-3">
                                                                <label class="form-label fw-semibold">Orden (Prioridad)</label>
                                                                <input type="number" class="form-control" name="order" value="{{ link.order }}" required>
                                                            </div>
                                                        </div>
"""
    
    # Find the row in inner_loop and replace
    row_start_idx = inner_loop.find('<div class="row">')
    row_end_idx = inner_loop.find('</div>\n                                                    </div>', row_start_idx)
    inner_loop = inner_loop[:row_start_idx] + edit_row_replacement + inner_loop[row_end_idx:]

    macro_end = """
                            {% endfor %}
                            {% if not section_links %}
                            <tr><td colspan="7" class="text-center text-muted py-3">No hay enlaces en esta sección.</td></tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% endmacro %}
        
        {{ render_links_table('Servicios Principales', links | selectattr('section', 'equalto', 'main') | list) }}
        {{ render_links_table('Tutoriales', links | selectattr('section', 'equalto', 'tutorial') | list) }}
        {{ render_links_table('Contacto de Soporte', links | selectattr('section', 'equalto', 'support') | list) }}
"""
    
    # Replace the whole <div class="card shadow-sm border-0 rounded-4"> up to </div>\n    </div>\n\n    <!-- Modal
    card_start = content.find('<div class="card shadow-sm border-0 rounded-4">')
    card_end = content.find('    <!-- Modal para Agregar Enlace -->')
    
    new_table_block = macro_start + inner_loop + macro_end + "\n"
    
    content = content[:card_start] + new_table_block + content[card_end:]
    
    # Now fix the Add Modal
    add_row_replacement = """
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label class="form-label fw-semibold">Sección</label>
                                <select class="form-select" name="section" required>
                                    <option value="main">Principal</option>
                                    <option value="tutorial">Tutoriales</option>
                                    <option value="support">Soporte</option>
                                </select>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label fw-semibold">Categoría</label>
                                <select class="form-select" name="category" required>
                                    <option value="comunes">Comunes</option>
                                    <option value="alumnos">Solo Alumnos</option>
                                    <option value="funcionarios">Solo Funcionarios</option>
                                </select>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label fw-semibold">Orden (Prioridad)</label>
                                <input type="number" class="form-control" name="order" value="100" required>
                            </div>
                        </div>
"""
    add_row_start = content.rfind('<div class="row">')
    add_row_end = content.find('</div>\n                    </div>\n                    <div class="modal-footer bg-light">', add_row_start)
    content = content[:add_row_start] + add_row_replacement + content[add_row_end:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    rewrite_admin()
