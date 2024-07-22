from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
from utils.token_utils import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify(dict(current_user))

@user_bp.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE users SET user_first_name = ?, user_last_name = ?, user_image = ?, university = ?, collections_paper_ids = ? WHERE user_id = ?',
                 (data.get('user_first_name', current_user['user_first_name']),
                  data.get('user_last_name', current_user['user_last_name']),
                  data.get('user_image', current_user['user_image']),
                  data.get('university', current_user['university']),
                  data.get('collections_paper_ids', current_user['collections_paper_ids']),
                  current_user['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Profile updated successfully'})
