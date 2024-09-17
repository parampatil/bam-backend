import sqlite3
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_connection import get_db_connection
from utils.token_utils import create_token
from utils.token_utils import token_required
from utils.token_utils import is_admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    # Incomming data format
    # {
    #     "user_email": "string",
    #     "user_first_name": "string",
    #     "user_last_name": "string",
    #     "user_password": "string",
    #     "university"?: "string",
    #     "user_image"?: "string",
    # }

    data = request.get_json()
    hashed_password = generate_password_hash(data['user_password'], method='sha256')
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (user_email, user_first_name, user_last_name, user_password, user_image, user_access, university, collections_paper_ids) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (data['user_email'], data['user_first_name'], data['user_last_name'], hashed_password, data.get('user_image',''), 'user', data.get('university', ''), ''))
        conn.commit()
        # user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400
    finally:
        conn.close()

    # token = create_token(user_id)
    
    response = {
        'message': 'Signed in successfully',
    }
    
    return jsonify(response)


@auth_bp.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_email = ?', (data['user_email'],)).fetchone()
    conn.close()
    if not user or not check_password_hash(user['user_password'], data['user_password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_token(user['user_id'])
    response = {
        'token': token,
        'user_first_name': user['user_first_name'],
        'user_last_name': user['user_last_name'],
    }
    return jsonify(response)

@auth_bp.route('/api/userimage', methods=['GET'])
@token_required
def userdata(current_user):
    user_data = {
        'user_image': current_user['user_image'],
    }
    return jsonify(user_data)

@auth_bp.route('/api/isadmin', methods=['GET'])
@token_required
def isadmin(current_user):
    if not current_user['user_access'] == 'admin':
        return jsonify({'message': 'Access denied'})

    return jsonify({'message': 'Admin'})
