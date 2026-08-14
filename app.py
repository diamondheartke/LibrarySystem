# app.py

from flask import Flask, render_template
from blueprints.api.router import api_bp
from database.database import Database

app = Flask(__name__)

# Ensure tables exist when starting the server
db = Database('test.db')
db.create_tables()
db.close()

# Register API Blueprint
app.register_blueprint(api_bp)

# Frontend Page Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
