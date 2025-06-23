from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import mysql.connector
import bcrypt
import jwt
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration de la base de données
db_config = {
    'host': os.getenv('MYSQL_HOST', 'mysql'),
    'user': os.getenv('MYSQL_USER', 'user'),
    'password': os.getenv('MYSQL_PASSWORD', 'userpass'),
    'database': os.getenv('MYSQL_DATABASE', 'users_db')
}

# Clé secrète pour JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

def get_db_connection():
    return mysql.connector.connect(**db_config)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split()[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ["username", "email", "password"]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (data['username'], data['email'], hashed_password)
        )
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'message': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ["username", "password"]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'is_admin': user['is_admin']
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'token': token,
                'is_admin': user['is_admin']
            })
        
        return jsonify({'message': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if current_user.get('is_admin'):
            cursor.execute("SELECT id, username, email, is_admin, created_at FROM users")
        else:
            cursor.execute("SELECT id, username, created_at FROM users")
        
        users = cursor.fetchall()
        return jsonify(users)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if not current_user.get('is_admin'):
        return jsonify({'message': 'Admin privileges required'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
