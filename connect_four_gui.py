import pygame
import sys
import numpy as np
import time
from connect_four_game import ConnectFour
from connect_four_ai import RandomAgent, MinimaxAgent, ImprovedMinimaxAgent

# Initialize pygame
pygame.init()

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Game constants
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
COLUMN_COUNT = 7
ROW_COUNT = 6

# Calculate dimensions
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE  # Extra row for piece animation and column selection
size = (width, height)

class ConnectFourGUI:
    """GUI for the Connect Four game using Pygame."""
    
    def __init__(self):
        """Initialize the GUI and game objects."""
        self.game = ConnectFour()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Connect Four')
        self.font = pygame.font.SysFont("monospace", 30)
        self.ai_agent = None
        self.human_player = 1
        self.ai_player = 2
        self.ai_thinking = False
        self.game_active = False
        self.main_menu = True
        
    def draw_board(self):
        """Draw the game board on the screen."""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw the area where pieces will drop
        pygame.draw.rect(self.screen, BLUE, (0, SQUARESIZE, width, height - SQUARESIZE))
        
        # Draw the grid and pieces
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Draw the grid cell
                pygame.draw.rect(self.screen, BLUE, 
                                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                
                # Draw the circle for the grid cell
                pygame.draw.circle(self.screen, BLACK, 
                                  (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                   int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), 
                                  RADIUS)
        
        # Draw the pieces
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.game.board[r, c] == 1:  # Player 1 (RED)
                    pygame.draw.circle(self.screen, RED, 
                                      (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                       int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                      RADIUS)
                elif self.game.board[r, c] == 2:  # Player 2 (YELLOW)
                    pygame.draw.circle(self.screen, YELLOW, 
                                      (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                       int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                      RADIUS)
        
        # Draw the hovering piece in the top area
        if self.game_active and not self.game.game_over and not self.ai_thinking:
            pos = pygame.mouse.get_pos()[0]
            color = RED if self.game.current_player == 1 else YELLOW
            pygame.draw.circle(self.screen, color, (pos, int(SQUARESIZE / 2)), RADIUS)
            
        # Draw game over message
        if self.game.game_over:
            self.draw_game_over_message()
            
        pygame.display.update()
        
    def draw_game_over_message(self):
        """Draw the game over message."""
        pygame.draw.rect(self.screen, WHITE, (0, 0, width, SQUARESIZE))
        
        if self.game.winner == 0:
            label = self.font.render("Game Over: Draw!", 1, BLUE)
        elif self.game.winner == self.human_player:
            label = self.font.render("Game Over: You Win!", 1, RED)
        else:
            label = self.font.render("Game Over: AI Wins!", 1, YELLOW)
            
        self.screen.blit(label, (width // 2 - label.get_width() // 2, 10))
        
        # Draw play again button
        pygame.draw.rect(self.screen, GRAY, (width // 2 - 100, SQUARESIZE // 2 + 10, 200, 40))
        play_again = self.font.render("Play Again", 1, BLACK)
        self.screen.blit(play_again, (width // 2 - play_again.get_width() // 2, 
                                       SQUARESIZE // 2 + 10 + play_again.get_height() // 2 - 5))
        
    def draw_main_menu(self):
        """Draw the main menu."""
        self.screen.fill(WHITE)
        
        # Title
        title = pygame.font.SysFont("monospace", 40).render("Connect Four", 1, BLUE)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 50))
        
        # AI difficulty buttons
        difficulties = [("Easy (Random)", RandomAgent), 
                       ("Medium (Minimax)", lambda: MinimaxAgent(max_depth=3)), 
                       ("Hard (Improved)", lambda: ImprovedMinimaxAgent(max_depth=4))]
        
        for i, (text, _) in enumerate(difficulties):
            y_pos = 150 + i * 80
            pygame.draw.rect(self.screen, GRAY, (width // 2 - 150, y_pos, 300, 60))
            button_text = self.font.render(text, 1, BLACK)
            self.screen.blit(button_text, (width // 2 - button_text.get_width() // 2, 
                                           y_pos + 30 - button_text.get_height() // 2))
        
        pygame.display.update()
        
    def handle_main_menu_click(self, pos):
        """Handle clicks in the main menu."""
        x, y = pos
        
        difficulties = [("Easy (Random)", RandomAgent), 
                       ("Medium (Minimax)", lambda: MinimaxAgent(max_depth=3)), 
                       ("Hard (Improved)", lambda: ImprovedMinimaxAgent(max_depth=4))]
        
        for i, (_, agent_class) in enumerate(difficulties):
            y_pos = 150 + i * 80
            if width // 2 - 150 <= x <= width // 2 + 150 and y_pos <= y <= y_pos + 60:
                self.ai_agent = agent_class() if not callable(agent_class) else agent_class()
                self.main_menu = False
                self.game_active = True
                self.start_new_game()
                break
                
    def handle_game_over_click(self, pos):
        """Handle clicks on the game over screen."""
        x, y = pos
        
        # Check if play again button was clicked
        if width // 2 - 100 <= x <= width // 2 + 100 and SQUARESIZE // 2 + 10 <= y <= SQUARESIZE // 2 + 50:
            self.main_menu = True
            self.game_active = False
            self.game = ConnectFour()
            
    def start_new_game(self):
        """Start a new game."""
        self.game = ConnectFour()
        self.game_active = True
        
    def animate_drop(self, column, player):
        """Animate the dropping of a piece."""
        # Find the row where the piece will land
        for row in range(ROW_COUNT-1, -1, -1):
            if self.game.board[row, column] == 0:
                break
                
        # Animate the drop
        for r in range(row+1):
            # Draw the board without the dropping piece
            self.draw_board()
            
            # Draw the dropping piece
            color = RED if player == 1 else YELLOW
            pygame.draw.circle(self.screen, color,
                              (int(column * SQUARESIZE + SQUARESIZE / 2),
                               int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                              RADIUS)
            pygame.display.update()
            pygame.time.wait(50)
            
    def get_ai_move(self):
        """Get the AI's move."""
        self.ai_thinking = True
        self.draw_board()
        
        # Small delay to show AI is "thinking"
        time.sleep(0.5)
        
        # Get the AI's move
        column = self.ai_agent.get_move(self.game)
        
        self.ai_thinking = False
        return column
            
    def run(self):
        """Run the game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEMOTION:
                    # Update the position of the hovering piece
                    if self.game_active and not self.game.game_over and not self.ai_thinking:
                        self.draw_board()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu:
                        self.handle_main_menu_click(event.pos)
                    elif self.game.game_over:
                        self.handle_game_over_click(event.pos)
                    elif self.game_active and self.game.current_player == self.human_player:
                        # Get the column the player clicked on
                        col = event.pos[0] // SQUARESIZE
                        
                        # Make the move if it's valid
                        if self.game.is_valid_move(col):
                            self.animate_drop(col, self.human_player)
                            self.game.make_move(col)
                            self.draw_board()
                            
                            # Check if the game is over
                            if self.game.game_over:
                                continue
                                
                            # AI's turn
                            if self.game.current_player == self.ai_player:
                                ai_col = self.get_ai_move()
                                if self.game.is_valid_move(ai_col):
                                    self.animate_drop(ai_col, self.ai_player)
                                    self.game.make_move(ai_col)
                                    self.draw_board()
            
            # Draw the current state
            if self.main_menu:
                self.draw_main_menu()
            else:
                self.draw_board()
                
            pygame.display.update()
            
if __name__ == "__main__":
    game_gui = ConnectFourGUI()
    game_gui.run()