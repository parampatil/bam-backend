from flask import Blueprint, request, jsonify
from utils.token_utils import token_required
from utils.db_connection import get_db_connection

collection_bp = Blueprint('collection_bp', __name__)

@collection_bp.route('/api/collections', methods=['GET'])
@token_required
def get_collections(current_user):
    conn = get_db_connection()
    collections_paper_ids = current_user['collections_paper_ids']
    if collections_paper_ids:
        paper_ids_list = [int(x) for x in collections_paper_ids.split(',') if x]
    else:
        paper_ids_list = []
    result = {'collections_paper_ids': paper_ids_list}
    conn.close()
    return jsonify(result)

@collection_bp.route('/api/collections/papers', methods=['GET'])
@token_required
def get_collections_papers(current_user):
    conn = get_db_connection()
    collections_paper_ids = current_user['collections_paper_ids']
    if collections_paper_ids:
        paper_ids_list = [int(x) for x in collections_paper_ids.split(',') if x]
    else:
        paper_ids_list = []
    
    result = []
    for paper_id in paper_ids_list:
        paper = conn.execute('SELECT * FROM research_papers WHERE paper_id = ?', (paper_id,)).fetchone()
        if paper:
            paper_data = {
                'paper_id': paper['paper_id'],
                'short_title': paper['short_paper_title'],
                'short_description': paper['short_description'],
                'preview_image': paper['preview_image'],
                'authors': [],
            }

            author_ids = paper['authors_ids']
            author_ids_list = [int(x) for x in author_ids.split(',')] if author_ids else []

            for author_id in author_ids_list:
                author = conn.execute('SELECT * FROM authors WHERE author_id = ?', (author_id,)).fetchone()
                if author:
                    author_data = {
                        'author_id': author['author_id'],
                        'first_name': author['author_first_name'],
                        'last_name': author['author_last_name'],
                        'image': author['author_image'],
                    }
                    paper_data['authors'].append(author_data)
            
            result.append(paper_data)

    conn.close()
    return jsonify(result)

@collection_bp.route('/api/collections', methods=['POST'])
@token_required
def add_to_collection(current_user):
    data = request.get_json()
    paper_id = data['paper_id']
    
    conn = get_db_connection()
    collections_paper_ids = current_user['collections_paper_ids']
    if collections_paper_ids:
        paper_ids_list = [int(x) for x in collections_paper_ids.split(',') if x]
    else:
        paper_ids_list = []
    
    if paper_id not in paper_ids_list:
        paper_ids_list.append(paper_id)
        updated_collections_paper_ids = ','.join(map(str, paper_ids_list))
        conn.execute('UPDATE users SET collections_paper_ids = ? WHERE user_id = ?', (updated_collections_paper_ids, current_user['user_id']))
        conn.commit()
        message = 'Paper added to collection'
    else:
        message = 'Paper already in collection'
    
    conn.close()
    return jsonify({'message': message})

@collection_bp.route('/api/collections/<int:paper_id>', methods=['DELETE'])
@token_required
def remove_from_collection(current_user, paper_id):
    conn = get_db_connection()
    collections_paper_ids = current_user['collections_paper_ids']
    if collections_paper_ids:
        paper_ids_list = [int(x) for x in collections_paper_ids.split(',') if x]
    else:
        paper_ids_list = []

    if paper_id in paper_ids_list:
        paper_ids_list.remove(paper_id)
        updated_collections_paper_ids = ','.join(map(str, paper_ids_list))
        conn.execute('UPDATE users SET collections_paper_ids = ? WHERE user_id = ?', (updated_collections_paper_ids, current_user['user_id']))
        conn.commit()
        message = 'Paper removed from collection'
    else:
        message = 'Paper not in collection'

    conn.close()
    return jsonify({'message': message})
