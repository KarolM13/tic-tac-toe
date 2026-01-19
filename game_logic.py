# LOGIKA GRY KÓŁKO-KRZYŻYK
import threading

class Game:
    def __init__(self):
        self.board = [' '] * 9
        self.turn = 'X'
        self.over = False
        self.winner = None
        
    def move(self, pos, symbol):
        if pos < 0 or pos > 8 or self.board[pos] != ' ' or symbol != self.turn:
            return False
            
        self.board[pos] = symbol
        
        # Check win
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for w in wins:
            if self.board[w[0]] == self.board[w[1]] == self.board[w[2]] == symbol:
                self.over = True
                self.winner = symbol
                return True
        
        # Check draw
        if ' ' not in self.board:
            self.over = True
            self.winner = 'DRAW'
            return True
        
        self.turn = 'O' if self.turn == 'X' else 'X'
        return True

class State:
    def __init__(self, max_players=2):
        self.game = None
        self.players = []
        self.lock = threading.Lock()
        self.max_players = max_players
    
    def add_player(self, email, nick):
        with self.lock:
            if len(self.players) >= self.max_players:
                return None
            symbol = 'X' if len(self.players) == 0 else 'O'
            self.players.append({'email': email, 'nick': nick, 'symbol': symbol})
            if len(self.players) == 2:
                self.game = Game()
            return symbol
    
    def make_move(self, symbol, pos, on_end_callback=None):
        with self.lock:
            if not self.game:
                return {'ok': False, 'error': 'Czekaj na 2 gracza'}
            if self.game.move(pos, symbol):
                if self.game.over and on_end_callback:
                    emails = [p['email'] for p in self.players]
                    on_end_callback(self.game, emails)
                return {'ok': True, 'board': self.game.board, 'turn': self.game.turn, 'over': self.game.over, 'winner': self.game.winner}
            return {'ok': False, 'error': 'Zły ruch'}
    
    def get_state(self):
        with self.lock:
            if not self.game:
                return {'started': False, 'players': len(self.players)}
            player_nicks = {p['symbol']: p['nick'] for p in self.players}
            return {'started': True, 'board': self.game.board, 'turn': self.game.turn, 'over': self.game.over, 'winner': self.game.winner, 'nicks': player_nicks}
    
    def reset(self):
        with self.lock:
            self.game = None
            self.players = []
