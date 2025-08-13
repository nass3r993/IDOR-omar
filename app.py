# Flask CTF Email Lab with UUID Ownership Check and UI Enhancements

from flask import Flask, request, render_template, redirect, session, jsonify, make_response, url_for
import sqlite3
import uuid
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supess4rsecretke2##@@3234y'

DB_PATH = 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    content TEXT)''')

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        admin_id = str(uuid.uuid4())
        hashed_pw = generate_password_hash("AdminnNE4$(444)")
        c.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (admin_id, 'admin', hashed_pw))
        c.execute("INSERT INTO messages (user_id, content) VALUES (?, ?)", (admin_id, 'Nass3r000{C0mma_Chang3s_Ev3ryth1ng}'))

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']
        uid = str(uuid.uuid4())
        hashed = generate_password_hash(pw)
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (uid, uname, hashed))
            msg = "Registered successfully."
        except:
            msg = "Username already exists."
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, password FROM users WHERE username=?", (uname,))
            user = cur.fetchone()
            if user and check_password_hash(user[1], pw):
                session['user_id'] = user[0]
                session['username'] = uname
                return redirect('/send')
            else:
                msg = "Invalid credentials."
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('session', '', expires=0)
    return resp

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        uname = request.form.get('username', '')
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username=?", (uname,))
            user = cur.fetchone()
            if user:
                return jsonify({"message": "If the user exists, a password reset link has been sent.", "uuid": user[0]})
        return jsonify({"message": "If the user exists, a password reset link has been sent."})
    return render_template('reset.html')

@app.route('/send')
def send():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('send.html', username=session['username'], user_id=session['user_id'])

@app.route('/api/users/messages')
def get_messages():
    uid_param = request.args.get('id', '')
    if not uid_param:
        return jsonify({"error": "Missing user ID"}), 400

    # Updated bypass logic to work properly
    uid_list = [u.strip() for u in uid_param.split(',') if u.strip()]
    target_uid = uid_list[-1]  # the actual target the bypasser wants

    # Enforce ownership check (against logged-in user only)
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Allow access if any one of the given UUIDs matches the logged-in user
    if session['user_id'] not in uid_list:
        return jsonify({"error": "Unauthorized access"}), 401

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT content FROM messages WHERE user_id=?", (target_uid,))
        messages = [row[0] for row in cur.fetchall()]
    return jsonify({"messages": messages})

@app.route('/flag-validation', methods=['GET', 'POST'])
def claim():
    if request.method == 'GET':
        return render_template('flag.html')

    data = request.get_json()
    submitted_flag = data.get('flag', '').strip()

    correct_flag = 'Nass3r000{C0mma_Chang3s_Ev3ryth1ng}'
    if submitted_flag == correct_flag:
        return jsonify({"success": True, "cert_url": "/static/GGG.png"})
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=False)
    app.run(host="0.0.0.0", port=3345)