# from flask import Flask, request, jsonify
# from models import db, GameData
# import pandas as pd
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
# db.init_app(app)

# @app.route('/upload', methods=['POST'])
# def upload_csv():
#     if 'file' not in request.files:
#         return "No file part", 400
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file", 400
    
#     file_path = os.path.join('uploads', file.filename)
#     file.save(file_path)
    
#     data = pd.read_csv(file_path)
#     with app.app_context():
#         for _, row in data.iterrows():
#             game_data = GameData(
#                 player=row['Name'],
#                 score=row['Price'],
#                 level=row['Positive'],
#                 timestamp=row['AppID']
#             )
#             db.session.add(game_data)
#         db.session.commit()
    
#     return "File uploaded and data saved to database", 201

# @app.route('/query', methods=['GET'])
# def query_data():
#     player = request.args.get('player')
#     score = request.args.get('score')
#     level = request.args.get('level')
#     timestamp = request.args.get('timestamp')
    
#     query = GameData.query
    
#     if player:
#         query = query.filter(GameData.player.contains(player))
#     if score:
#         query = query.filter_by(score=score)
#     if level:
#         query = query.filter_by(level=level)
#     if timestamp:
#         query = query.filter_by(timestamp=timestamp)
    
#     results = query.all()
#     return jsonify([result.to_dict() for result in results])

# if __name__ == '__main__':
#     if not os.path.exists('uploads'):
#         os.makedirs('uploads')
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


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
