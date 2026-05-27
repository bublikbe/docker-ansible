import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
app = Flask(__name__, static_folder='static', static_url_path='')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
def init_db():
    print("Initializing database...")
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialization complete.")
            break
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying in 3 seconds...")
            time.sleep(3)
            retries -= 1
    else:
        print("Could not connect to database to run migrations. Continuing...")
@app.route('/')
def index():
    return app.send_static_file('index.html')
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, username, email, password FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve users: {str(e)}"}), 500
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, JSON payload is required"}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"error": "Fields 'username', 'email', and 'password' are required"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id;",
            (username, email, password)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User created successfully", "id": user_id}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
if __name__ == '__main__':

    init_db()

    app.run(host='0.0.0.0', port=5000)
