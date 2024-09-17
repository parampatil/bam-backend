from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
from utils.token_utils import token_required
from werkzeug.security import generate_password_hash
from utils.token_utils import is_email_unique
from werkzeug.security import check_password_hash

user_bp = Blueprint('user', __name__)


@user_bp.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user data
    user_data = dict(current_user)

    # Remove sensitive information
    user_data.pop('collections_paper_ids', None)
    user_data.pop('user_password', None)

    # Fetch paper titles
    paper_ids = current_user['collections_paper_ids']
    if paper_ids:
        paper_ids_list = paper_ids.split(',')
        cursor.execute('SELECT paper_id, short_paper_title FROM research_papers WHERE paper_id IN ({})'.format(
            ','.join('?' * len(paper_ids_list))), paper_ids_list)
        papers = cursor.fetchall()
        user_data['paper_collections'] = {
            paper['paper_id']: paper['short_paper_title'] for paper in papers}
    else:
        user_data['paper_collections'] = {}

    conn.close()
    return jsonify(user_data)


@user_bp.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the new email already exists in the database
    new_email = data.get('user_email', current_user['user_email'])
    if new_email != current_user['user_email'] and not is_email_unique(new_email):
        return jsonify({'message': 'Email already exists'}), 400

    cursor.execute('UPDATE users SET user_first_name = ?, user_last_name = ?, user_image = ?, university = ?, user_email = ? WHERE user_id = ?',
                   (data.get('user_first_name', current_user['user_first_name']),
                    data.get('user_last_name', current_user['user_last_name']),
                    data.get('user_image', current_user['user_image']),
                    data.get('university', current_user['university']),
                    new_email,
                    current_user['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Profile updated successfully'})


@user_bp.route('/api/profile', methods=['DELETE'])
@token_required
def delete_profile(current_user):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE user_id = ?',
                 (current_user['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Profile deleted successfully'})


@user_bp.route('/api/change-password', methods=['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    print(current_user['user_password'], data['old_password'])
    print(check_password_hash(current_user['user_password'], data['old_password']))

    # Check if the old password is correct
    if not check_password_hash(current_user['user_password'], data['old_password']):
        return jsonify({'message': 'Incorrect old password'}), 400

    cursor.execute('UPDATE users SET user_password = ? WHERE user_id = ?',
                   (generate_password_hash(data['new_password']), current_user['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Password changed successfully'})