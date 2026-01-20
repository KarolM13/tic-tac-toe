# BAZA DANYCH - SQLAlchemy + PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Game(db.Model):
    """Model reprezentujący zapisaną grę w bazie danych"""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    player_x_email = db.Column(db.String(120), nullable=False)
    player_x_nick = db.Column(db.String(80), nullable=False)
    player_o_email = db.Column(db.String(120), nullable=False)
    player_o_nick = db.Column(db.String(80), nullable=False)
    board = db.Column(db.String(200), nullable=False)  # JSON string - zwiększone do 200
    winner = db.Column(db.String(10))  # 'X', 'O', 'DRAW', or NULL for ongoing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # 'completed', 'ongoing'
    
    def to_dict(self):
        """Konwertuje obiekt Game do słownika"""
        return {
            'id': self.id,
            'player_x': {
                'email': self.player_x_email,
                'nick': self.player_x_nick
            },
            'player_o': {
                'email': self.player_o_email,
                'nick': self.player_o_nick
            },
            'board': json.loads(self.board) if isinstance(self.board, str) else self.board,
            'winner': self.winner,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Tworzy obiekt Game ze słownika"""
        return Game(
            player_x_email=data.get('player_x_email'),
            player_x_nick=data.get('player_x_nick'),
            player_o_email=data.get('player_o_email'),
            player_o_nick=data.get('player_o_nick'),
            board=json.dumps(data.get('board', [' '] * 9)),
            winner=data.get('winner'),
            status=data.get('status', 'completed')
        )
    
    def __repr__(self):
        return f'<Game {self.id}: {self.player_x_nick} vs {self.player_o_nick}>'


def init_db(app):
    """Inicjalizacja bazy danych"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[DB] Baza danych zainicjalizowana!")
