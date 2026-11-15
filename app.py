from flask import Flask, request, session, redirect, render_template_string
import sqlite3, bcrypt, os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Session secure ah iruka

# Database create pannu
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password BLOB)')
    conn.commit()
    conn.close()
init_db()

HTML = """
<h2>Secure Login System</h2>
<a href='/register'>Register</a> | <a href='/login'>Login</a> | <a href='/dashboard'>Dashboard</a> | <a href='/logout'>Logout</a>
<hr>
{{msg}}
<form method='POST'>
Username: <input name='username' required><br><br>
Password: <input type='password' name='password' required><br><br>
<input type='submit' value='Submit'>
</form>
"""

@app.route('/register', methods=['GET','POST'])
def register():
    msg = ""
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password'].encode()
        # bcrypt la password ah hash pannurom - plain ah store panna matom
        hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
        try:
            # SQL Injection protection: ? placeholder use pannurom
            conn = sqlite3.connect('users.db')
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed))
            conn.commit()
            conn.close()
            msg = "Registered Successfully! Now Login"
        except:
            msg = "Username already exists!"
    return render_template_string(HTML, msg=msg)

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ""
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password'].encode()
        conn = sqlite3.connect('users.db')
        # SQL Injection protection
        cur = conn.execute("SELECT password FROM users WHERE username=?", (user,))
        row = cur.fetchone()
        conn.close()
        if row and bcrypt.checkpw(pwd, row[0]):
            session['user'] = user # Session create aagudhu
            return redirect('/dashboard')
        else:
            msg = "Invalid Login!"
    return render_template_string(HTML, msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return f"<h2>Welcome {session['user']}!</h2><p>You are logged in securely.</p><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.clear() # Session clear pannurom
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
