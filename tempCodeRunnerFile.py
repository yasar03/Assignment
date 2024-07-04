from flask import Flask, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

DATABASE = 'game_data.db'

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS games (
        Unnamed INTEGER,
        AppID INTEGER PRIMARY KEY,
        Name TEXT,
        ReleaseDate TEXT,
        RequiredAge INTEGER,
        Price REAL,
        DLCount INTEGER,
        AboutGame TEXT,
        SupportedLanguages TEXT,
        Windows BOOLEAN,
        Mac BOOLEAN,
        Linux BOOLEAN,
        Positive INTEGER,
        Negative INTEGER,
        ScoreRank INTEGER,
        Developers TEXT,
        Publishers TEXT,
        Categories TEXT,
        Genres TEXT,
        Tags TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Welcome to the Game Data API!"

# Route to upload CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        df = pd.read_csv(file)
        conn = sqlite3.connect(DATABASE)
        df.to_sql('games', conn, if_exists='replace', index=False)
        conn.close()
        return jsonify({'message': 'File successfully uploaded'}), 200

# Route to query data
@app.route('/query', methods=['GET'])
def query_data():
    filters = request.args.to_dict()
    query = "SELECT * FROM games WHERE "

    conditions = []
    for key, value in filters.items():
        if key in ['RequiredAge', 'Price', 'DLCount', 'Positive', 'Negative', 'ScoreRank']:
            conditions.append(f"{key} = {value}")
        else:
            conditions.append(f"{key} LIKE '%{value}%'")

    query += " AND ".join(conditions)
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_json(orient='records')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
