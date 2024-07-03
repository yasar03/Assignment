from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(80))
    score = db.Column(db.Integer)
    level = db.Column(db.Integer)
    timestamp = db.Column(db.String(80))
    
    def to_dict(self):
        return {
            'player': self.player,
            'score': self.score,
            'level': self.level,
            'timestamp': self.timestamp
        }
