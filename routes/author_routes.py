from flask import Blueprint, request, jsonify
from utils.token_utils import token_required
from utils.db_connection import get_db_connection

author_bp = Blueprint('author', __name__)

@author_bp.route('/api/authors', methods=['POST'])
# @token_required
def add_author():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO authors (author_first_name, author_last_name, author_image) VALUES (?, ?, ?, ?)',
                 (data['author_first_name'], data['author_last_name'], data['author_image']))
    conn.commit()
    author_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'message': 'Author added successfully', 'author_id': author_id})

@author_bp.route('/api/authors/all', methods=['GET'])
def list_authors():
    conn = get_db_connection()
    
    authors = conn.execute('SELECT * FROM authors').fetchall()
    result = []

    for author in authors:
        author_data = {
            'author_id': author['author_id'],
            'author_first_name': author['author_first_name'],
            'author_last_name': author['author_last_name'],
            'author_image': author['author_image'],
            'author_papers': []
        }

        # Fetch papers associated with the author
        papers = conn.execute('SELECT paper_id, short_paper_title FROM research_papers WHERE authors_ids LIKE ?', 
                              (f'%{author["author_id"]}%',)).fetchall()

        for paper in papers:
            paper_data = {
                'paper_id': paper['paper_id'],
                'short_paper_title': paper['short_paper_title']
            }
            author_data['author_papers'].append(paper_data)
        
        result.append(author_data)

    conn.close()
    return jsonify(result)

@author_bp.route('/api/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    # Authorization header
    auth_header = request.headers.get('Authorization')
    # if auth_header is None or not auth_header.startswith('Bearer '):
    #     return jsonify({'message': 'Unauthorized'}), 401

    # token = auth_header.split(' ')[1]
    # if not is_admin(token):
    #     return jsonify({'message': 'Forbidden'}), 403

    data = request.get_json()
    author_first_name = data.get('author_first_name')
    author_last_name = data.get('author_last_name')
    author_image = data.get('author_image')
    
    if not author_first_name or not author_last_name or not author_image:
        return jsonify({'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    try:
        # Update the author's information in the database
        result = conn.execute('''
            UPDATE authors
            SET author_first_name = ?, author_last_name = ?, author_image = ?
            WHERE author_id = ?
        ''', (author_first_name, author_last_name, author_image, author_id))
        
        conn.commit()

        # Check if the author was updated
        if result.rowcount == 0:
            return jsonify({'message': 'Author not found'}), 404

    except Exception as e:
        conn.close()
        return jsonify({'message': str(e)}), 500

    conn.close()
    return jsonify({'message': 'Author updated successfully'})


@author_bp.route('/api/authors/<int:author_id>', methods=['DELETE'])

def delete_author(author_id):
    # user_id = get_jwt_identity()  # Get the user id from the JWT token
    # if not is_admin(user_id):
    #     return jsonify({"message": "Unauthorized"}), 403
    conn = get_db_connection()
   
    try:
        conn.execute('DELETE FROM authors WHERE author_id = ?', (author_id,))
        conn.commit()

        if conn.rowcount == 0:
            return jsonify({"message": "Author not found"}), 404

        return jsonify({"message": "Author deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting author", "error": str(e)}), 500
    finally:
        conn.close()





