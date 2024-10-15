from flask import Flask, render_template, redirect, request, url_for
import os

import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')

app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def home():
    cursor = db.databes.cursor()
    cursor.execute('SELECT * FROM usuarios')

    myresult = cursor.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObject)

@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuarios(username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.comnit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.comnit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)

