from flask import Flask, request, jsonify

app = Flask(__name__)

# Estructura en memoria
incidencias = []
contador = 1

@app.route('/incidencias', methods=['POST'])
def crear_incidencia():
    global contador
    data = request.get_json()
    incidencia = {
        'id': contador,
        'titulo': data.get('titulo'),
        'descripcion': data.get('descripcion'),
        'prioridad': data.get('prioridad', 'media'),
        'estado': 'abierta',
        'responsable': data.get('responsable', None),
        'fecha_cierre': None
    }
    incidencias.append(incidencia)
    contador += 1
    return jsonify(incidencia), 201

@app.route('/incidencias', methods=['GET'])
def listar_incidencias():
    return jsonify(incidencias)

@app.route('/incidencias/<int:id>', methods=['GET'])
def ver_incidencia(id):
    for incidencia in incidencias:
        if incidencia['id'] == id:
            return jsonify(incidencia)
    return jsonify({'error': 'Incidencia no encontrada'}), 404

@app.route('/incidencias/<int:id>', methods=['PATCH'])
def actualizar_incidencia(id):
    data = request.get_json()
    for incidencia in incidencias:
        if incidencia['id'] == id:
            # Actualiza cualquier campo proporcionado
            for clave in ['titulo', 'descripcion', 'prioridad', 'estado', 'responsable']:
                if clave in data:
                    incidencia[clave] = data[clave]
            # Si el estado se marca como 'cerrada', guarda fecha_cierre
            if data.get('estado') == 'cerrada':
                from datetime import datetime
                incidencia['fecha_cierre'] = datetime.now().isoformat()
            return jsonify(incidencia)
    return jsonify({'error': 'Incidencia no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
