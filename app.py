from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
app = Flask(__name__)

# Conectar a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('burgas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la base de datos y una tabla (si no existe)
def init_db():
    conn = get_db_connection()
    conn.close()

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/menu_pedido')
def menu_pedido():
    return render_template('menu_pedido.html')

@app.route('/pedidos')
def pedidos():
    conn = get_db_connection()
    pedidoss = conn.execute('SELECT * FROM pedidos').fetchall()
    conn.close()
    return render_template('pedidos.html',pedidos = pedidoss)

@app.route('/update_pedido', methods=['POST'])
def update_pedido():
    pedido_id = request.form['id']
    pedido = request.form['pedido']
    estado = request.form['estado']

    conn = get_db_connection()
    conn.execute('UPDATE pedidos SET pedido = ?, estado = ? WHERE id = ?', (pedido, estado, pedido_id))
    conn.commit()
    conn.close()

    return redirect(url_for('pedidos'))

# Ruta para agregar un item a la base de datos
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json  # Obtener datos en formato JSON
    pedido = data['pedido']
    estado = 'sin confirmar'
    
    conn = get_db_connection()
    conn.execute('INSERT INTO pedidos (pedido,estado) VALUES (?,?)', (pedido,estado))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Item agregado exitosamente!"})

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True)
