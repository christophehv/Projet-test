from http.server import BaseHTTPRequestHandler
import json
import os
import mysql.connector

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')
            return

        # Exemple de récupération des champs du formulaire
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Connexion à la base de données (adapter les variables d'environnement)
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', ''),
                database=os.environ.get('DB_NAME', 'test')
            )
            cursor = conn.cursor()
            # Exemple d'insertion (à adapter selon ton schéma SQL)
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Erreur base de données: {str(e)}'.encode())
            return

        self.send_response(201)
        self.end_headers()
        self.wfile.write(b'Inscription OK')

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b"Method Not Allowed") 