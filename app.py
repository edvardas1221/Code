from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import random
app = Flask(__name__)
app.secret_key = 'RETR0'
DB_NAME = 'auth.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

@app.route("/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone():
                flash("Toks vartotojo vardas jau egzistuoja!")
                return redirect(url_for('register'))

            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registracija sėkminga, galite prisijungti.')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()

        if user:
            session['username'] = username
            flash('Sėkmingai prisijungėte!')
            return redirect(url_for('menu'))
        else:
            flash('Neteisingas vartotojo vardas arba slaptažodis')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/menu")
def menu():
    if 'username' not in session:
        flash("Prašome prisijungti")
        return redirect(url_for('login'))

    return render_template('menu.html', username=session['username'])


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('Sėkmingai atsijungėte')
    return redirect(url_for("login"))

@app.route('/game1')
def game1():
    return render_template('game1.html')

@app.route("/game2")
def game2():
    return render_template("game2.html")

@app.route('/secret')
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)
