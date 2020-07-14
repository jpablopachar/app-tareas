from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexión a base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbtareas'

mysql = MySQL(app)

# Configuraciones
app.secret_key = "miClaveSecreta"

# Rutas
@app.route('/')
def Index():
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM tarea')

    data = cur.fetchall()

    cur.close()

    return render_template('index.html', tasks = data)

@app.route('/agregar', methods=['POST'])
def addTask():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO tarea (titulo, descripcion) VALUES (%s, %s)", (title, description))
        mysql.connection.commit()
        flash('La tarea se ha agregado correctamente!')

        return redirect(url_for('Index'))

@app.route('/editar/<id>', methods = ['POST', 'GET'])
def getTask(id):
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM tarea WHERE idTarea = %s', (id))

    data = cur.fetchall()

    cur.close()

    return render_template('edit-task.html', task = data[0])

@app.route('/actualizar/<id>', methods=['POST'])
def updateTask(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()

        cur.execute("""UPDATE tarea SET titulo = %s, descripcion = %s WHERE idTarea = %s """, (title, description, id))
        flash('La tarea fue editada correctamente!')
        mysql.connection.commit()

        return redirect(url_for('Index'))

@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def deleteTask(id):
    cur = mysql.connection.cursor()

    cur.execute('DELETE FROM tarea WHERE idTarea = {0}'.format(id))
    mysql.connection.commit()
    flash('La tarea fue eliminada correctamente!')

    return redirect(url_for('Index'))

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(port=3000, debug=True)
