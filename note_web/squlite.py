from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_data_db():
    connection = sqlite3.connect('web.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY, ask TEXT, answer TEXT)''')
    connection.commit()
    connection.close()

@app.route('/')
def index():
    connection = sqlite3.connect('web.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return render_template('web.html', tasks=tasks)

@app.route('/s', methods=['POST'])
def add_ask():
    ask = request.form['ask']
    connection = sqlite3.connect('web.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (ask) VALUES (?)", (ask,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:ask_id>')
def delete_ask(ask_id):
    connection = sqlite3.connect('web.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (ask_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_data_db()

    app.run(debug=False)
    