from flask import Blueprint, request, jsonify
from utils.token_utils import token_required
from utils.db_connection import get_db_connection

author_bp = Blueprint('author', __name__)

@author_bp.route('/api/authors', methods=['POST'])
# @token_required
def add_author():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO authors (author_first_name, author_last_name, author_image, author_website) VALUES (?, ?, ?, ?)',
                 (data['author_first_name'], data['author_last_name'], data['author_image'], data['author_website']))
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

@author_bp.route('/api/authors/', methods=['PUT'])
def update_author():
    data = request.get_json()
    author_id = data.get('author_id')
    author_first_name = data.get('author_first_name')
    author_last_name = data.get('author_last_name')
    author_image = data.get('author_image')
    
    if not author_id or not author_first_name or not author_last_name or not author_image:
        return jsonify({'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    try:
        # Update the author's information in the database
        conn.execute('''
            UPDATE authors
            SET author_first_name = ?, author_last_name = ?, author_image = ?
            WHERE author_id = ?
        ''', (author_first_name, author_last_name, author_image, author_id))
        
        conn.commit()

        # Check if the author was updated
        if conn.total_changes == 0:
            return jsonify({'message': 'Author not found'}), 404

    except Exception as e:
        conn.close()
        return jsonify({'message': str(e)}), 500

    conn.close()
    return jsonify({'message': 'Author updated successfully'})




