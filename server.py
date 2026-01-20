# SERWER KÓŁKO-KRZYŻYK - FLASK
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
from datetime import datetime
from game_logic import State
from database import db, Game as GameModel, init_db
import os
import json
import requests

app = Flask(__name__)
CORS(app)

# Konfiguracja bazy danych
# Dla PostgreSQL: postgresql://user:password@localhost/dbname
# Dla SQLite (prostsza opcja): sqlite:///games.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja bazy danych
init_db(app)

MAX_PLAYERS = 2
state = State(MAX_PLAYERS)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/join', methods=['POST'])
def join():
    email = request.json.get('email')
    nick = request.json.get('nick')
    if not email or not nick:
        return jsonify({'error': 'Brak email lub nick'}), 400
    symbol = state.add_player(email, nick)
    if not symbol:
        return jsonify({'error': 'Pełne'}), 400
    return jsonify({'symbol': symbol})

@app.route('/api/state')
def get_state():
    return jsonify(state.get_state())

@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    
    def on_end(game, emails):
        threading.Thread(target=send_email, args=(game, emails), daemon=True).start()
        threading.Thread(target=save_log, args=(game,), daemon=True).start()
    
    result = state.make_move(data['symbol'], data['pos'], on_end)
    if result['ok']:
        return jsonify(result)
    return jsonify(result), 400

@app.route('/api/reset', methods=['POST'])
def reset():
    state.reset()
    return jsonify({'ok': True})


# ===== REST API CRUD DLA GIER =====

@app.route('/api/games', methods=['POST'])
def create_game():
    """CREATE - Tworzy nową grę w bazie danych"""
    try:
        data = request.json
        game = GameModel.from_dict(data)
        db.session.add(game)
        db.session.commit()
        return jsonify({'ok': True, 'game': game.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/games', methods=['GET'])
def get_all_games():
    """READ - Pobiera wszystkie gry z bazy danych"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = GameModel.query.order_by(GameModel.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        games = [game.to_dict() for game in pagination.items]
        return jsonify({
            'ok': True,
            'games': games,
            'total': pagination.total,
            'page': page,
            'pages': pagination.pages
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """READ - Pobiera pojedynczą grę po ID"""
    try:
        game = GameModel.query.get_or_404(game_id)
        return jsonify({'ok': True, 'game': game.to_dict()})
    except Exception as e:
        return jsonify({'ok': False, 'error': 'Gra nie znaleziona'}), 404

@app.route('/api/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    """UPDATE - Aktualizuje istniejącą grę"""
    try:
        game = GameModel.query.get_or_404(game_id)
        data = request.json
        
        if 'player_x_email' in data:
            game.player_x_email = data['player_x_email']
        if 'player_x_nick' in data:
            game.player_x_nick = data['player_x_nick']
        if 'player_o_email' in data:
            game.player_o_email = data['player_o_email']
        if 'player_o_nick' in data:
            game.player_o_nick = data['player_o_nick']
        if 'board' in data:
            game.board = json.dumps(data['board'])
        if 'winner' in data:
            game.winner = data['winner']
        if 'status' in data:
            game.status = data['status']
        
        game.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'ok': True, 'game': game.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """DELETE - Usuwa grę z bazy danych"""
    try:
        game = GameModel.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return jsonify({'ok': True, 'message': 'Gra usunięta'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/games/stats', methods=['GET'])
def get_stats():
    """Dodatkowy endpoint - statystyki gier"""
    try:
        total_games = GameModel.query.count()
        x_wins = GameModel.query.filter_by(winner='X').count()
        o_wins = GameModel.query.filter_by(winner='O').count()
        draws = GameModel.query.filter_by(winner='DRAW').count()
        
        return jsonify({
            'ok': True,
            'stats': {
                'total_games': total_games,
                'x_wins': x_wins,
                'o_wins': o_wins,
                'draws': draws
            }
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


# ===== INTEGRACJA Z ZEWNĘTRZNYM API =====

@app.route('/api/quote', methods=['GET'])
def get_quote():
    """Pobiera losowy cytat/poradę z zewnętrznego API"""
    try:
        # Próbujemy kilka API jako backup
        apis = [
            {
                'url': 'https://api.adviceslip.com/advice',
                'parse': lambda r: {'quote': r['slip']['advice'], 'author': 'Advice Slip'}
            },
            {
                'url': 'http://api.adviceslip.com/advice',
                'parse': lambda r: {'quote': r['slip']['advice'], 'author': 'Advice Slip'}
            },
            {
                'url': 'https://api.quotable.io/random',
                'parse': lambda r: {'quote': r['content'], 'author': r['author']}
            }
        ]
        
        for api in apis:
            try:
                response = requests.get(api['url'], timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    parsed = api['parse'](data)
                    return jsonify({
                        'ok': True,
                        'quote': parsed['quote'],
                        'author': parsed['author']
                    })
            except:
                continue
        
        return jsonify({'ok': False, 'error': 'Nie udało się pobrać cytatu z żadnego API'}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# SMTP
def send_email(game, emails):
    print(f"\n[SMTP] Wysyłam email do: {emails}")
    try:
        from smtp_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
        import smtplib
        from email.mime.text import MIMEText
        
        result = "REMIS" if game.winner == 'DRAW' else f"Wygrał {game.winner}"
        body = f"Wynik: {result}\nData: {datetime.now()}\nPlansza: {game.board}"
        
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        for email in emails:
            msg = MIMEText(body)
            msg['Subject'] = f"Gra: {result}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = email
            smtp.send_message(msg)
        
        smtp.quit()
        print("[SMTP] Wysłano!")
    except Exception as e:
        print(f"[SMTP] Błąd: {e}")

# FTP
def save_log(game):
    """Zapisuje grę do bazy danych"""
    print("\n[DATABASE] Zapisuję grę do bazy danych...")
    try:
        with app.app_context():
            # Pobierz dane graczy
            players = state.players
            if len(players) < 2:
                print("[DATABASE] Brak wystarczającej liczby graczy")
                return
            
            player_x = next((p for p in players if p['symbol'] == 'X'), None)
            player_o = next((p for p in players if p['symbol'] == 'O'), None)
            
            if not player_x or not player_o:
                print("[DATABASE] Nie znaleziono graczy")
                return
            
            # Utwórz rekord w bazie
            game_record = GameModel(
                player_x_email=player_x['email'],
                player_x_nick=player_x['nick'],
                player_o_email=player_o['email'],
                player_o_nick=player_o['nick'],
                board=json.dumps(game.board),
                winner=game.winner,
                status='completed'
            )
            
            db.session.add(game_record)
            db.session.commit()
            
            print(f"[DATABASE] Zapisano grę ID: {game_record.id}")
    except Exception as e:
        print(f"[DATABASE] Błąd: {e}")
        with app.app_context():
            db.session.rollback()

if __name__ == "__main__":
    print("="*50)
    print("  SERWER: http://127.0.0.1:5555")
    print("="*50)
    app.run(host='0.0.0.0', port=5555, debug=False)
