from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

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

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html', title="Login")

# http://localhost:5000/pythonlogin/register
# This will be the registration page, we need to use both GET and POST requests
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

        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, email, password))
        mysql.connection.commit()

        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# http://localhost:5000/pythinlogin/home
# This will be the home page, only accessible for logged-in users
@app.route('/')
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        # User is logged in show them the home page
        return render_template('home/home.html', username=session['username'], title="Home")
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'loggedin' in session:
        # User is logged in show them the home page
        return render_template('auth/profile.html', username=session['username'], title="Profile")
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
