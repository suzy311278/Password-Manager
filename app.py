from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory storage for simplicity (use a database in production)
users = {'admin': 'admin123'}
passwords = []

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']
        name = request.form.get('name')
        website = request.form.get('website')
        if action == 'generate':
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            passwords.append({'name': name, 'password': password, 'website': website})
        elif action == 'edit':
            new_password = request.form.get('new_password')
            for entry in passwords:
                if entry['name'] == name:
                    entry['password'] = new_password
                    entry['website'] = website

    return render_template('dashboard.html', passwords=passwords)

if __name__ == '__main__':
    app.run(debug=True)
