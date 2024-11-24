from flask import Flask, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

app = Flask(__name__)
socketio = SocketIO(app)  # Inicializar SocketIO

@app.route('/receive-nfc', methods=['POST'])
def receive_nfc():
    # Obtener los datos del NFC enviados desde el lector (la cédula)
    nfc_data = request.form.get('nfcData')

    # Definir la ruta del archivo de estudiantes y leer su contenido
    archivo_estudiantes = 'archivos/estudiantes.txt'
    nombre_completo = None

    if os.path.exists(archivo_estudiantes):
        with open(archivo_estudiantes, 'r') as archivo:
            for linea in archivo:
                cedula, nombre, apellido = linea.strip().split(',')
                if cedula == nfc_data:
                    nombre_completo = f"{nombre} {apellido}"
                    break

    # Si no se encuentra el nombre, se devuelve un mensaje de error
    if not nombre_completo:
        return jsonify({'mensaje': 'Estudiante no encontrado.'}), 404

    # Obtener la fecha y hora actual del sistema
    fecha_hora = datetime.now().strftime('%Y-%m-%d,%H:%M')

    # Definir la ruta del archivo de ingresos
    archivo_ingresos = 'archivos/ingresos.txt'

    # Verificar si el archivo existe y obtener el último registro de la cédula
    ultimo_registro = None
    if os.path.exists(archivo_ingresos):
        with open(archivo_ingresos, 'r') as archivo:
            for linea in archivo:
                registro = linea.strip().split(',')
                if registro[0] == nfc_data:
                    ultimo_registro = registro

    # Determinar el tipo de registro: si el último es "ENTRADA", se guarda como "SALIDA" y viceversa.
    if ultimo_registro and ultimo_registro[3] == 'ENTRADA':
        tipo_registro = 'SALIDA'
    else:
        tipo_registro = 'ENTRADA'

    # Formato de la línea a guardar en el archivo
    nueva_linea = f"{nfc_data},{fecha_hora},{tipo_registro}\n"

    # Guardar la línea en el archivo ingresos.txt
    with open(archivo_ingresos, 'a') as archivo:
        archivo.write(nueva_linea)

    # Enviar el mensaje de saludo
    mensaje_saludo = f"BIENVENIDO(A) {nombre_completo}" if tipo_registro == 'ENTRADA' else f"HASTA LUEGO {nombre_completo}"

    # Emitir el mensaje a todos los clientes conectados mediante WebSocket
    socketio.emit('nfc_response', {'mensaje': mensaje_saludo})

    return jsonify({'mensaje': mensaje_saludo})

@app.route('/listado', methods=['GET'])
def obtener_listado():
    # Leer los datos del archivo de ingresos
    archivo_ingresos = 'archivos/ingresos.txt'
    registros = []
    if os.path.exists(archivo_ingresos):
        with open(archivo_ingresos, 'r') as archivo:
            for linea in archivo:
                # Dividir la línea por comas y agregar a la lista de registros
                datos = linea.strip().split(',')
                registros.append({
                    'cedula': datos[0],
                    'fecha': datos[1],
                    'hora': datos[2],
                    'tipo_registro': datos[3]
                })
    return jsonify(registros)

@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

