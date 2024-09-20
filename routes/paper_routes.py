from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
from utils.token_utils import token_required
from utils.token_utils import is_admin
import json

paper_bp = Blueprint('paper', __name__)

#region List Papers:
@paper_bp.route('/api/papers', methods=['GET'])
def list_papers():
    conn = get_db_connection()
    
    papers = conn.execute('SELECT paper_id, paper_created_by_user_id, short_paper_title, short_description, preview_image, authors_ids, paper_publishDate FROM research_papers').fetchall()

    result = []

    for paper in papers:
        paper_data = {
            'paper_id': paper['paper_id'],
            'short_paper_title': paper['short_paper_title'],
            'paper_publishDate': paper['paper_publishDate'],
            'short_description': paper['short_description'],
            'preview_image': paper['preview_image'],
            'authors': [],
        }

        author_ids = paper['authors_ids']
        author_ids_list = [int(x) for x in author_ids.strip('[]').split(',')] if author_ids else []

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

#region Get Paper by ID:
@paper_bp.route('/api/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    conn = get_db_connection()
    
    paper = conn.execute('SELECT * FROM research_papers WHERE paper_id = ?', (paper_id,)).fetchone()
    
    if not paper:
        conn.close()
        return jsonify({'message': 'Paper not found'}), 404

    paper_data = {
        'paper_id': paper['paper_id'],
        'authors': [],
        'paper_html': paper['paper_html'],
        'paper_css': paper['paper_css']
    }

    author_ids = paper['authors_ids']
    if author_ids:
        author_ids_list = [int(x) for x in author_ids.strip('[]').split(',')] if author_ids else []

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

    conn.close()
    return jsonify(paper_data)

#region Get Paper List:
@paper_bp.route('/api/papers/edit', methods=['GET'])
def list_papers_short_response():
    conn = get_db_connection()

    papers = conn.execute('SELECT paper_id, short_paper_title, paper_publishDate, short_description, preview_image, paper_created_by_user_id FROM research_papers').fetchall()

    result = []
    for paper in papers:
        user = conn.execute('SELECT user_first_name, user_last_name FROM users WHERE user_id = ?', (paper['paper_created_by_user_id'],)).fetchone()
        paper_data = {
            'paper_id': paper['paper_id'],
            'short_paper_title': paper['short_paper_title'],
            'paper_publishDate': paper['paper_publishDate'],
            'short_description': paper['short_description'],
            'preview_image': paper['preview_image'],
            'paper_created_by_user_name': f'{user["user_first_name"]} {user["user_last_name"]}' if user else None
        }
        result.append(paper_data)

    conn.close()
    return jsonify(result)

#region Get Paper Card by ID:
@paper_bp.route('/api/papers/editcard/<int:paper_id>', methods=['GET'])
def get_paper_for_editcard(paper_id):
    conn = get_db_connection()
    
    paper = conn.execute('''
        SELECT paper_id, paper_created_by_user_id, short_paper_title, paper_publishDate, short_description, preview_image, authors_ids
        FROM research_papers
        WHERE paper_id = ?
    ''', (paper_id,)).fetchone()

    if not paper:
        conn.close()
        return jsonify({'message': 'Paper not found'}), 404
    
    if paper['paper_created_by_user_id']:
        user = conn.execute('SELECT user_first_name, user_last_name FROM users WHERE user_id = ?', (paper['paper_created_by_user_id'],)).fetchone()
        user_name = f'{user["user_first_name"]} {user["user_last_name"]}' if user else None
    else:
        user_name = None

    paper_data = {
        'paper_id': paper['paper_id'],
        'paper_created_by_user_name': user_name,
        'short_paper_title': paper['short_paper_title'],
        'paper_publishDate': paper['paper_publishDate'],
        'short_description': paper['short_description'],
        'preview_image': paper['preview_image'],
        'authors': [],
    }

    author_ids = paper['authors_ids']
    if author_ids:
        author_ids_list = [int(x) for x in author_ids.strip('[]').split(',')] if author_ids else []

        for author_id in author_ids_list:
            author = conn.execute('SELECT * FROM authors WHERE author_id = ?', (author_id,)).fetchone()
            if author:
                author_data = {
                    'author_id': author['author_id'],
                    'first_name': author['author_first_name'],
                    'last_name': author['author_last_name'],
                    'image': author['author_image']
                }
                paper_data['authors'].append(author_data)

    conn.close()
    return jsonify(paper_data)

#region Edit Paper Card by ID:
@paper_bp.route('/api/papers/editcard/<int:paper_id>', methods=['PUT'])
def edit_paper_card(paper_id):
    token = request.headers.get('Authorization').replace('Bearer ', '')
    
    conn = get_db_connection()
    data = request.get_json()
    
    required_fields = ['paper_id', 'short_paper_title', 'paper_publishDate', 'short_description', 'preview_image', 'authors']
    for field in required_fields:
        if field not in data:
            conn.close()
            return jsonify({'message': f'Missing {field} in request body'}), 400
    
    paper_data = {
        'paper_id': data['paper_id'],
        'short_paper_title': data['short_paper_title'],
        'paper_publishDate': data['paper_publishDate'],
        'short_description': data['short_description'],
        'preview_image': data['preview_image'],
        'authors_ids': ','.join(map(str, data['authors'])),
    }

    conn.execute('''
        UPDATE research_papers
        SET short_paper_title = ?,
            paper_publishDate = ?,
            short_description = ?,
            preview_image = ?,
            authors_ids = ?
        WHERE paper_id = ?
    ''', (paper_data['short_paper_title'],
      paper_data['paper_publishDate'],
      paper_data['short_description'],
      paper_data['preview_image'],
      paper_data['authors_ids'],
      paper_data['paper_id']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Paper card updated successfully'})

#region Get Paper Content by ID:
@paper_bp.route('/api/papers/content/<int:paper_id>', methods=['GET'])
def get_paper_editor_content(paper_id):
    auth_header = request.headers.get('Authorization')

    conn = get_db_connection()

    paper = conn.execute('''
        SELECT paper_id, paper_editor 
        FROM research_papers 
        WHERE paper_id = ?
    ''', (paper_id,)).fetchone()

    conn.close()

    if not paper:
        return jsonify({'message': 'Paper not found'}), 404

    if paper['paper_editor']:
        paper_editor = json.loads(paper['paper_editor'])
    else:
        paper_editor = {}

    response_data = {
        'paper_id': paper['paper_id'],
        'paper_editor': paper_editor
    }

    return jsonify(response_data)

#region Edit Paper Content by ID: 
@paper_bp.route('/api/papers/content/<int:paper_id>', methods=['POST'])
def edit_paper_content(paper_id):
    conn = get_db_connection()
    data = request.get_json()

    paper_editor = data.get('paper_editor')

    if not paper_editor:
        return jsonify({"message": "Invalid request"}), 400

    conn.execute('''
        UPDATE research_papers 
        SET paper_editor = ? 
        WHERE paper_id = ?
    ''', (json.dumps(paper_editor), paper_id))

    conn.commit()
    return jsonify({"message": "Paper content updated successfully"}), 200

#region Delete Paper ID:
@paper_bp.route('/api/papers/<int:paper_id>', methods=['DELETE'])
@is_admin
def delete_paper(paper_id):

    if not paper_id:
        return jsonify({"message": "Missing paper_id"}), 400
    
    conn = get_db_connection()
    c = conn.cursor()

    users = c.execute('''
        SELECT user_id, collections_paper_ids
        FROM users
        WHERE collections_paper_ids LIKE ?
    ''', (f'%{paper_id}%',)).fetchall()

    for user in users:
        collections_paper_ids = user['collections_paper_ids'].split(',')
        collections_paper_ids = [id for id in collections_paper_ids if id != str(paper_id)]
        new_collections_paper_ids = ','.join(collections_paper_ids)
        
        c.execute('''
            UPDATE users
            SET collections_paper_ids = ?
            WHERE user_id = ?
        ''', (new_collections_paper_ids, user['user_id']))
    
    c.execute('''
        DELETE FROM research_papers 
        WHERE paper_id = ?
    ''', (paper_id,))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Paper deleted successfully"}), 200

#region Publish Paper by ID: 
@paper_bp.route('/api/papers/publish/<int:paper_id>', methods=['PUT'])
def publish_paper(paper_id):
    data = request.get_json()
    paper_id_from_body = data.get('paper_id')
    paper_html = data.get('paper_html')
    paper_css = data.get('paper_css')
    
    if not paper_id_from_body or not paper_html or not paper_css:
        return jsonify({'message': 'Missing required fields'}), 400

    if paper_id != int(paper_id_from_body):
        return jsonify({'message': 'Paper ID mismatch'}), 400

    conn = get_db_connection()
    try:
        result = conn.execute('''
            UPDATE research_papers
            SET paper_html = ?, paper_css = ?
            WHERE paper_id = ?
        ''', (paper_html, paper_css, paper_id))
        
        conn.commit()

        if result.rowcount == 0:
            return jsonify({'message': 'Paper not found'}), 404

    except Exception as e:
        conn.close()
        return jsonify({'message': str(e)}), 500

    conn.close()
    return jsonify({'message': 'Paper published successfully'})

#region Create Paper Card:
@paper_bp.route('/api/papers/createcard', methods=['POST'])
@token_required
def create_paper_card(current_user):
    data = request.get_json()

    short_paper_title = data.get('short_paper_title')
    paper_publishDate = data.get('paper_publishDate')
    short_description = data.get('short_description')
    preview_image = data.get('preview_image')
    authors_ids = data.get('authors_ids')

    authors_ids = ','.join(map(str, authors_ids)) if authors_ids else ''

    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO research_papers (paper_created_by_user_id, short_paper_title, paper_publishDate, short_description, preview_image, authors_ids)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (current_user['user_id'], short_paper_title, paper_publishDate, short_description, preview_image, authors_ids))

        conn.commit()

    except Exception as e:
        conn.close()
        return jsonify({'message': str(e)}), 500

    conn.close()
    return jsonify({'message': 'Paper created successfully'}), 201
