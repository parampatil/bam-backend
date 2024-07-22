from flask import Blueprint, request, jsonify
from utils.token_utils import token_required
from utils.db_connection import get_db_connection

author_bp = Blueprint('author', __name__)

@author_bp.route('/api/authors', methods=['POST'])
@token_required
def add_author(current_user):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO authors (author_first_name, author_last_name, author_image, author_website) VALUES (?, ?, ?, ?)',
                 (data['author_first_name'], data['author_last_name'], data['author_image'], data['author_website']))
    conn.commit()
    author_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'message': 'Author added successfully', 'author_id': author_id})

