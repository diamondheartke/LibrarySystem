# app.py

from flask import Flask, render_template, session, redirect
from blueprints.api.router import api_bp
from database.database import Database

app = Flask(__name__)
app.secret_key = 'LibraySystemSecretKey'

# Ensures tables exist when starting the server
db = Database('test.db')
db.create_tables()
db.close()

# Registering API Blueprint
app.register_blueprint(api_bp)

# login check
def login_check():
    return session.get('login_state', False)

# On-enter route
@app.route('/')
def index():
    return redirect('/loading')

# Loading page route
@app.route('/loading')
def loading():
    return render_template('loading.html')

# Home page route
@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
