# SERWER KÓŁKO-KRZYŻYK - FLASK
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
from datetime import datetime
from game_logic import State

app = Flask(__name__)
CORS(app)

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
    print("\n[FTP] Zapisuję log...")
    import os
    if not os.path.exists("game_logs"):
        os.makedirs("game_logs")
    
    result = "REMIS" if game.winner == 'DRAW' else f"Wygrał {game.winner}"
    filename = f"game_logs/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Data: {datetime.now()}\nWynik: {result}\nPlansza: {game.board}")
    
    print(f"[FTP] Zapisano: {filename}")

if __name__ == "__main__":
    print("="*50)
    print("  SERWER: http://127.0.0.1:5555")
    print("="*50)
    app.run(host='0.0.0.0', port=5555, debug=False)
