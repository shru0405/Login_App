from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt  # Ensure to install the 'bcrypt' library, pip install bcrpyt

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e6d7g8h9i10'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*********'  # Replace ******* with your database password.
app.config['MYSQL_DB'] = 'loginapp'

# Initialize MySQL
mysql = MySQL(app)

# Define a function to check certain conditions before each request
@app.before_request
def check_request():
    if request.endpoint in ['login', 'register', 'static', 'favicon', 'favicon.ico']:
        return None
    if 'loggedin' not in session:
        return redirect(url_for('login'))

# Hash the password securely
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Login route
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and bcrypt.checkpw(password.encode('utf-8'), account['password']):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html', title="Login")

# Registration route
@app.route('/pythonlogin/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Incomplete data"}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username LIKE %s", [username])
        account = cursor.fetchone()

        if account:
            return jsonify({"error": "Account already exists"}), 400

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({"error": "Invalid email address"}), 400

        if not re.match(r'[A-Za-z0-9]+', username):
            return jsonify({"error": "Username must contain only characters and numbers"}), 400

        hashed_password = hash_password(password)

        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, email, hashed_password))
        mysql.connection.commit()

        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Home route
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home/home.html', username=session['username'], title="Home")
    return redirect(url_for('login'))

# Profile route
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('auth/profile.html', username=session['username'], title="Profile")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
