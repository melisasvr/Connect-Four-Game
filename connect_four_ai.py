import numpy as np
import random
from connect_four_game import ConnectFour

class RandomAgent:
    """Agent that chooses moves randomly from available valid moves."""
    
    def get_move(self, game):
        """Return a random valid move."""
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        return random.choice(valid_moves) if valid_moves else -1

class MinimaxAgent:
    """Agent that uses the minimax algorithm to choose moves."""
    
    def __init__(self, max_depth=3):
        """Initialize with a maximum search depth."""
        self.max_depth = max_depth
        
    def get_move(self, game):
        """Return the best move according to minimax."""
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        if not valid_moves:
            return -1
            
        best_score = float('-inf')
        best_move = valid_moves[0]
        
        for col in valid_moves:
            # Create a copy of the game to simulate moves
            game_copy = ConnectFour()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player
            
            game_copy.make_move(col)
            score = self._minimax(game_copy, self.max_depth-1, False)
            
            if score > best_score:
                best_score = score
                best_move = col
                
        return best_move
        
    def _minimax(self, game, depth, is_maximizing):
        """Minimax algorithm implementation."""
        # Terminal states
        if game.game_over:
            if game.winner == 0:  # Draw
                return 0
            elif is_maximizing:  # Opponent won
                return -100
            else:  # Agent won
                return 100
                
        if depth == 0:
            return self._evaluate_board(game.board, game.current_player)
            
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        
        if is_maximizing:
            value = float('-inf')
            for col in valid_moves:
                game_copy = ConnectFour()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player
                
                game_copy.make_move(col)
                value = max(value, self._minimax(game_copy, depth-1, False))
            return value
        else:
            value = float('inf')
            for col in valid_moves:
                game_copy = ConnectFour()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player
                
                game_copy.make_move(col)
                value = min(value, self._minimax(game_copy, depth-1, True))
            return value
            
    def _evaluate_board(self, board, player):
        """Simple board evaluation function."""
        # This is a very basic evaluation - a better one would look for potential wins
        opponent = 3 - player  # Switch between player 1 and 2
        score = 0
        
        # Check horizontal, vertical and diagonal lines for potential wins
        # This is simplified - a real implementation would be more sophisticated
        return random.randint(-10, 10)  # Placeholder for simple evaluation

class ImprovedMinimaxAgent(MinimaxAgent):
    """Enhanced minimax agent with alpha-beta pruning and better evaluation."""
    
    def get_move(self, game):
        """Return the best move using alpha-beta pruning."""
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        if not valid_moves:
            return -1
            
        best_score = float('-inf')
        best_move = valid_moves[0]
        alpha = float('-inf')
        beta = float('inf')
        
        for col in valid_moves:
            # Create a copy of the game to simulate moves
            game_copy = ConnectFour()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player
            
            game_copy.make_move(col)
            score = self._alpha_beta(game_copy, self.max_depth-1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = col
                
            alpha = max(alpha, best_score)
                
        return best_move
        
    def _alpha_beta(self, game, depth, alpha, beta, is_maximizing):
        """Minimax with alpha-beta pruning."""
        # Terminal states
        if game.game_over:
            if game.winner == 0:  # Draw
                return 0
            elif is_maximizing:  # Opponent won
                return -100
            else:  # Agent won
                return 100
                
        if depth == 0:
            return self._evaluate_board(game.board, game.current_player)
            
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        
        if is_maximizing:
            value = float('-inf')
            for col in valid_moves:
                game_copy = ConnectFour()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player
                
                game_copy.make_move(col)
                value = max(value, self._alpha_beta(game_copy, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            return value
        else:
            value = float('inf')
            for col in valid_moves:
                game_copy = ConnectFour()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player
                
                game_copy.make_move(col)
                value = min(value, self._alpha_beta(game_copy, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value
            
    def _evaluate_board(self, board, player):
        """Improved board evaluation function."""
        opponent = 3 - player  # Switch between player 1 and 2
        
        # Count sequences of 2 and 3 in a row for both players
        player_score = self._count_sequences(board, player)
        opponent_score = self._count_sequences(board, opponent)
        
        return player_score - opponent_score
        
    def _count_sequences(self, board, player):
        """Count sequences of 2 and 3 in a row for the given player."""
        rows, cols = board.shape
        score = 0
        
        # Check horizontal sequences
        for r in range(rows):
            for c in range(cols - 3):
                window = [board[r, c + i] for i in range(4)]
                score += self._evaluate_window(window, player)
                
        # Check vertical sequences
        for c in range(cols):
            for r in range(rows - 3):
                window = [board[r + i, c] for i in range(4)]
                score += self._evaluate_window(window, player)
                
        # Check diagonal sequences (positive slope)
        for r in range(rows - 3):
            for c in range(cols - 3):
                window = [board[r + i, c + i] for i in range(4)]
                score += self._evaluate_window(window, player)
                
        # Check diagonal sequences (negative slope)
        for r in range(3, rows):
            for c in range(cols - 3):
                window = [board[r - i, c + i] for i in range(4)]
                score += self._evaluate_window(window, player)
                
        return score
        
    def _evaluate_window(self, window, player):
        """Score a window of 4 positions."""
        opponent = 3 - player
        
        if window.count(player) == 4:
            return 100  # Winning position
        elif window.count(player) == 3 and window.count(0) == 1:
            return 5  # Three in a row
        elif window.count(player) == 2 and window.count(0) == 2:
            return 2  # Two in a row
        elif window.count(opponent) == 3 and window.count(0) == 1:
            return -4  # Block opponent's three in a row
            
        return 0