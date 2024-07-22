from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
from utils.token_utils import token_required

paper_bp = Blueprint('paper', __name__)

@paper_bp.route('/api/papers', methods=['GET'])
def list_papers():
    conn = get_db_connection()
    
    papers = conn.execute('SELECT * FROM research_papers').fetchall()
    result = []

    for paper in papers:
        paper_data = {
            'paper_id': paper['paper_id'],
            'created_by': paper['paper_created_by_user_id'],
            'short_title': paper['short_paper_title'],
            'short_description': paper['short_description'],
            'preview_image': paper['preview_image'],
            'authors': [],
            'paper_pdf_link': paper['paper_pdf_link']
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
                    'website': author['author_website']
                }
                paper_data['authors'].append(author_data)
        
        result.append(paper_data)

    conn.close()
    return jsonify(result)

@paper_bp.route('/api/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    conn = get_db_connection()
    paper = conn.execute('SELECT * FROM research_papers WHERE paper_id = ?', (paper_id,)).fetchone()
    
    if not paper:
        conn.close()
        return jsonify({'message': 'Paper not found'}), 404
    
    paper_data = {
        'paper_id': paper['paper_id'],
        'created_by': paper['paper_created_by_user_id'],
        'short_title': paper['short_paper_title'],
        'short_description': paper['short_description'],
        'preview_image': paper['preview_image'],
        'authors': [],
        'paper_pdf_link': paper['paper_pdf_link'],
        'paper_description': paper['paper_description']
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
                    'website': author['author_website']
                }
                paper_data['authors'].append(author_data)

    conn.close()
    return jsonify(paper_data)

@paper_bp.route('/api/papers', methods=['POST'])
@token_required
def add_paper(current_user):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO research_papers (paper_created_by_user_id, short_paper_title, short_description, preview_image, authors_ids, paper_pdf_link, paper_description) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (current_user['user_id'], data['short_paper_title'], data['short_description'], data['preview_image'], ','.join(map(str, data['authors_ids'])), data['paper_pdf_link'], data['paper_description']))
    conn.commit()
    paper_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'message': 'Paper added successfully', 'paper_id': paper_id})
