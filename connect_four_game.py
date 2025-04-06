import numpy as np
import random

class ConnectFour:
    """
    Implementation of the Connect Four game with the core game logic.
    """
    
    def __init__(self):
        """Initialize the game board and game state."""
        # Board dimensions: 6 rows x 7 columns
        self.rows = 6
        self.columns = 7
        
        # Create empty board (0 = empty, 1 = player 1, 2 = player 2/AI)
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        
        # Initialize game state
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def is_valid_move(self, column):
        """
        Check if a move is valid (column is not full).
        
        Args:
            column (int): The column index (0-based) to check
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        # Check if column is within bounds
        if column < 0 or column >= self.columns:
            return False
            
        # Check if the column is not full (top row is empty)
        return self.board[0, column] == 0
        
    def get_valid_moves(self):
        """
        Get a list of all valid moves (columns that are not full).
        
        Returns:
            list: List of column indices where a move is valid
        """
        return [col for col in range(self.columns) if self.is_valid_move(col)]
        
    def make_move(self, column):
        """
        Make a move in the specified column.
        
        Args:
            column (int): The column index (0-based) to place the piece
            
        Returns:
            bool: True if the move was successful, False if invalid
        """
        # Check if the game is already over
        if self.game_over:
            return False
            
        # Check if the move is valid
        if not self.is_valid_move(column):
            return False
            
        # Find the lowest empty row in the column
        for row in range(self.rows-1, -1, -1):
            if self.board[row, column] == 0:
                # Place the current player's piece
                self.board[row, column] = self.current_player
                
                # Check if this move results in a win
                if self.check_win(row, column):
                    self.game_over = True
                    self.winner = self.current_player
                # Check if the board is full (draw)
                elif len(self.get_valid_moves()) == 0:
                    self.game_over = True
                    self.winner = 0  # Draw
                else:
                    # Switch to the other player
                    self.current_player = 3 - self.current_player  # Toggle between 1 and 2
                
                return True
        
        # This should never happen if is_valid_move is called first
        return False
    
    def check_win(self, row, col):
        """
        Check if the last move at (row, col) resulted in a win.
        
        Args:
            row (int): Row of the last move
            col (int): Column of the last move
            
        Returns:
            bool: True if the move resulted in a win, False otherwise
        """
        player = self.board[row, col]
        
        # Check horizontally
        def check_horizontal():
            for c in range(max(0, col-3), min(col+1, self.columns-3)):
                if all(self.board[row, c+i] == player for i in range(4)):
                    return True
            return False
            
        # Check vertically
        def check_vertical():
            if row <= self.rows - 4:
                return all(self.board[row+i, col] == player for i in range(4))
            return False
            
        # Check diagonally (up-right)
        def check_diagonal_up_right():
            for r, c in zip(range(min(3, row), max(-1, row-3), -1), 
                           range(max(0, col-3), min(col+1, self.columns-3))):
                if all(self.board[r-i, c+i] == player for i in range(4)):
                    return True
            return False
            
        # Check diagonally (down-right)
        def check_diagonal_down_right():
            for r, c in zip(range(max(0, row-3), min(row+1, self.rows-3)), 
                           range(max(0, col-3), min(col+1, self.columns-3))):
                if all(self.board[r+i, c+i] == player for i in range(4)):
                    return True
            return False
            
        return (check_horizontal() or check_vertical() or 
                check_diagonal_up_right() or check_diagonal_down_right())
    
    def print_board(self):
        """Print the current state of the board."""
        # Print column numbers
        print(' '.join(str(i) for i in range(self.columns)))
        
        # Print board with players' pieces
        for row in range(self.rows):
            row_str = ''
            for col in range(self.columns):
                if self.board[row, col] == 0:
                    row_str += '. '
                elif self.board[row, col] == 1:
                    row_str += 'X '
                else:  # self.board[row, col] == 2
                    row_str += 'O '
            print(row_str.strip())
            
    def get_game_result(self):
        """
        Get the result of the game.
        
        Returns:
            int: 0 for draw, 1 if player 1 won, 2 if player 2 won, None if game is not over
        """
        if not self.game_over:
            return None
        return self.winner

class RandomAgent:
    """A simple agent that makes random valid moves."""
    
    def select_move(self, game):
        """
        Select a random valid move.
        
        Args:
            game (ConnectFour): The current game state
            
        Returns:
            int: The column to play in
        """
        valid_moves = game.get_valid_moves()
        if valid_moves:
            return random.choice(valid_moves)
        return None

def play_human_vs_ai(ai_agent):
    """
    Function to allow a human to play against the AI.
    
    Args:
        ai_agent: The AI agent to play against
    """
    game = ConnectFour()
    
    while not game.game_over:
        game.print_board()
        print(f"Player {game.current_player}'s turn")
        
        if game.current_player == 1:  # Human player
            try:
                column = int(input("Enter column (0-6): "))
                if not game.make_move(column):
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid integer.")
        else:  # AI player
            column = ai_agent.select_move(game)
            print(f"AI chooses column: {column}")
            game.make_move(column)
    
    # Game over
    game.print_board()
    if game.winner == 0:
        print("Game ended in a draw!")
    else:
        print(f"Player {game.winner} wins!")

if __name__ == "__main__":
    # Example usage: Play against a random AI
    random_agent = RandomAgent()
    play_human_vs_ai(random_agent)