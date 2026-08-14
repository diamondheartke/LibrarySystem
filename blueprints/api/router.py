# blueprints/api/router.py

from flask import Blueprint
from blueprints.api.books.routes import books_bp

# Main API parent blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Nest sub-blueprints under /api/books
api_bp.register_blueprint(books_bp, url_prefix='/books')
