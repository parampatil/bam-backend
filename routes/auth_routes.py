import sqlite3
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_connection import get_db_connection
from utils.token_utils import create_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['user_password'], method='sha256')
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (user_email, user_first_name, user_last_name, user_password, user_access, university, collections_paper_ids) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (data['user_email'], data['user_first_name'], data['user_last_name'], hashed_password, 'user', data.get('university', ''), ''))
        conn.commit()
        user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400
    finally:
        conn.close()

    token = create_token(user_id)
    return jsonify({'message': 'User created successfully', 'token': token})

@auth_bp.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_email = ?', (data['user_email'],)).fetchone()
    conn.close()
    if not user or not check_password_hash(user['user_password'], data['user_password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_token(user['user_id'])
    return jsonify({'message': 'Signed in successfully', 'token': token})
