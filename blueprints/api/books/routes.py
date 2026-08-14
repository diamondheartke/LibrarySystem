# blueprints/api/books/routes.py

from flask import Blueprint, jsonify, request
from database.database import Database

books_bp = Blueprint('books', __name__)
db = Database('test.db')

@books_bp.route('/display')#@books_bp.route('/display', methods=['GET'])
def get_books():
    records = db.get_all('book_records')
    # Format database tuples into JSON-friendly dictionaries
    books = [
        {
            "id": r[0], "book_id": r[1], "title": r[2],
            "subject": r[3], "author": r[4], "isbn": r[5], "status": r[6]
        }
        for r in records
    ]
    return jsonify({"status": "success", "data": books}), 200

@books_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()
    required = ['book_id', 'title', 'subject', 'author', 'isbn', 'status']
    
    if not data or not all(k in data for k in required):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
    db.insert_book_records(data)
    return jsonify({"status": "success", "message": "Book added successfully"}), 201
