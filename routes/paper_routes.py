from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
from utils.token_utils import token_required
import json
paper_bp = Blueprint('paper', __name__)

@paper_bp.route('/api/papers', methods=['GET'])
def list_papers():
    conn = get_db_connection()
    
    papers = conn.execute('SELECT paper_id, paper_created_by_user_id, short_paper_title, short_description, preview_image, authors_ids, paper_pdf_link, paper_description, paper_publishDate FROM research_papers').fetchall()

    
    result = []

    for paper in papers:
        
        paper_data = {
            'paper_id': paper['paper_id'],
            # 'paper_created_by_user_id': paper['paper_created_by_user_id'],  # Adjusted the key name
            'short_paper_title': paper['short_paper_title'],  # Adjusted the key name
            'paper_publishDate': paper['paper_publishDate'],  # Added paper_publishDate field
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
                }
                paper_data['authors'].append(author_data)
        
        result.append(paper_data)

    conn.close()
    return jsonify(result)


@paper_bp.route('/api/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    conn = get_db_connection()
    
    # Fetch the paper from the database
    paper = conn.execute('SELECT * FROM research_papers WHERE paper_id = ?', (paper_id,)).fetchone()
    
    if not paper:
        conn.close()
        return jsonify({'message': 'Paper not found'}), 404

    # Create the paper data structure
    paper_data = {
        'paper_id': paper['paper_id'],
        # 'paper_created_by_user_id': paper['paper_created_by_user_id'],
        # 'short_paper_title': paper['short_paper_title'],
        # 'short_description': paper['short_description'],
        # 'preview_image': paper['preview_image'],
        'authors': [],
        # 'paper_pdf_link': paper['paper_pdf_link'],
        'paper_description': {
            'paper_html': paper['paper_html'],
            'paper_css': paper['paper_css']
        }
    }

    # Process authors if available
    author_ids = paper['authors_ids']
    if author_ids:
        # Convert the author_ids string to a list of integers
        author_ids_list = [int(x) for x in author_ids.strip('[]').split(',')] if author_ids else []

        for author_id in author_ids_list:
            # Fetch author details
            author = conn.execute('SELECT * FROM authors WHERE author_id = ?', (author_id,)).fetchone()
            if author:
                # Create author data structure
                author_data = {
                    'author_id': author['author_id'],
                    'first_name': author['author_first_name'],
                    'last_name': author['author_last_name'],
                    'image': author['author_image'],
                    # 'website': author['author_website']
                }
                # Append the author data to the authors list
                paper_data['authors'].append(author_data)

    # Close the database connection
    conn.close()

    # Return the final JSON response
    return jsonify(paper_data)


@paper_bp.route('/api/papers/edit', methods=['GET'])
def list_papers_short_response():
    conn = get_db_connection()

    # Fetch the list of papers along with the creator's name
    papers = conn.execute('''
        SELECT rp.paper_id, u.user_first_name || ' ' || u.user_last_name AS paper_created_by_user_name, rp.short_paper_title, rp.paper_publishDate, rp.short_description, rp.preview_image
        FROM research_papers rp
        JOIN users u ON rp.paper_created_by_user_id = u.user_id
    ''').fetchall()

    conn.close()

    # Format the response
    result = []
    for paper in papers:
        paper_data = {
            'paper_id': paper['paper_id'],
            'paper_created_by_user_name': paper['paper_created_by_user_name'],
            'short_paper_title': paper['short_paper_title'],
            'paper_publishDate': paper['paper_publishDate'],
            'short_description': paper['short_description'],
            'preview_image': paper['preview_image']
        }
        result.append(paper_data)

    # Return the JSON response
    return jsonify(result)




# def check_admin(token):
#     # Implement the logic to check if the user is an admin using the token
#     # This is a placeholder; replace it with your actual admin check logic
#     # For example:
#     # user = get_user_from_token(token)
#     # return user['user_access'] == 'admin'
#     return True

@paper_bp.route('/api/papers/editcard/<int:paper_id>', methods=['GET'])
def get_paper_for_editcard(paper_id):
    # Get the token from the request headers
    # token = request.headers.get('Authorization').replace('Bearer ', '')
    
    # if not check_admin(token):
    #     return jsonify({'message': 'Unauthorized access'}), 403

    conn = get_db_connection()
    
    # Fetch the paper from the database
    paper = conn.execute('''
        SELECT paper_id, short_paper_title, paper_publishDate, short_description, preview_image, paper_html, paper_css, authors_ids
        FROM research_papers
        WHERE paper_id = ?
    ''', (paper_id,)).fetchone()

    if not paper:
        conn.close()
        return jsonify({'message': 'Paper not found'}), 404

    # Create the paper data structure
    paper_data = {
        'paper_id': paper['paper_id'],
        'short_paper_title': paper['short_paper_title'],
        'paper_publishDate': paper['paper_publishDate'],
        'short_description': paper['short_description'],
        'preview_image': paper['preview_image'],
        'authors': [],
        'paper_description': {
            'paper_html': paper['paper_html'],
            'paper_css': paper['paper_css']
        }
    }

    # Process authors if available
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

    # Return the JSON response
    return jsonify(paper_data)



@paper_bp.route('/api/papers/editcard/<int:paper_id>', methods=['PUT'])
def edit_paper_card(paper_id):
    token = request.headers.get('Authorization').replace('Bearer ', '')
    
    # if not check_admin(token):
    #     return jsonify({'message': 'Unauthorized access'}), 403
    
    conn = get_db_connection()
    data = request.get_json()
    
    # Validate and parse request body
    required_fields = ['paper_id', 'short_paper_title', 'paper_publishDate', 'short_description', 'preview_image', 'authors', 'paper_description']
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
        'authors_ids': ','.join(map(str, data['authors'])),  # Convert list of author ids to comma-separated string
        'paper_html': data['paper_description']['paper_html'],
        'paper_css': data['paper_description']['paper_css']
    }

    # Update the paper in the database
    conn.execute('''
        UPDATE research_papers
        SET short_paper_title = ?,
            paper_publishDate = ?,
            short_description = ?,
            preview_image = ?,
            authors_ids = ?,
            paper_html = ?,
            paper_css = ?
        WHERE paper_id = ?
    ''', (paper_data['short_paper_title'],
      paper_data['paper_publishDate'],
      paper_data['short_description'],
      paper_data['preview_image'],
      paper_data['authors_ids'],
      paper_data['paper_html'],
      paper_data['paper_css'],
      paper_data['paper_id']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Paper card updated successfully'})




@paper_bp.route('/api/papers/editcard/content/<int:paper_id>', methods=['GET'])
def get_paper_editor_content(paper_id):
    # Ensure the request is authorized and the user is an admin
    auth_header = request.headers.get('Authorization')
    # if not auth_header or not is_admin(auth_header):
    #     return jsonify({'message': 'Unauthorized'}), 403

    conn = get_db_connection()

    # Fetch the paper with the paper_editor field
    paper = conn.execute('''
        SELECT paper_id, paper_editor 
        FROM research_papers 
        WHERE paper_id = ?
    ''', (paper_id,)).fetchone()

    conn.close()

    if not paper:
        return jsonify({'message': 'Paper not found'}), 404

    # Convert the paper_editor field from JSON to a Python dictionary
    paper_editor = json.loads(paper['paper_editor'])

    # Create the response
    response_data = {
        'paper_id': paper['paper_id'],
        'paper_editor': paper_editor
    }

    return jsonify(response_data)


@paper_bp.route('/api/papers/editcard/content/<int:paper_id>', methods=['PUT'])
def edit_paper_content(paper_id):
    token = request.headers.get('Authorization')
    # if not verify_admin(token):  # Function to verify if user is an admin
    #     return jsonify({"message": "Unauthorized"}), 403
    conn = get_db_connection()


    data = request.get_json()
    paper_editor = data.get('paper_editor')

    if not paper_editor:
        return jsonify({"message": "Invalid request"}), 400

    # Update query
    conn.execute('''
        UPDATE research_papers 
        SET paper_editor = ? 
        WHERE paper_id = ?
    ''', (json.dumps(paper_editor), paper_id))

    conn.commit()
    return jsonify({"message": "Paper content updated successfully"}), 200


@paper_bp.route('/api/papers/editcard/content/<int:paper_id>', methods=['DELETE'])
def delete_paper(paper_id):
    # token = request.headers.get('Authorization')
    # if not verify_admin(token):
    #     return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    if data.get('paper_id') != paper_id:
        return jsonify({"message": "Paper ID mismatch"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        DELETE FROM research_papers 
        WHERE paper_id = ?
    ''', (paper_id,))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Paper deleted successfully"}), 200




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
