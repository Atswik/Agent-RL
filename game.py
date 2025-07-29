import numpy as np
import pygame as pxl
import random
import pickle

pxl.init()

COLS, ROWS = 3, 3
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 8
SPACE = 22

CIRCLE_IMG = pxl.image.load('assets/circle.png')
CROSS_IMG = pxl.image.load('assets/cross.png')

CIRCLE_IMG = pxl.transform.smoothscale(CIRCLE_IMG, (SQUARE_SIZE - 2 * SPACE, SQUARE_SIZE - 2 * SPACE))
CROSS_IMG = pxl.transform.smoothscale(CROSS_IMG, (SQUARE_SIZE - 2 * SPACE, SQUARE_SIZE - 2 * SPACE))

RED = (255, 0, 0)
BG_COLOR = (21, 21, 21)
LINE_COLOR = (203, 203, 203)
CIRCLE_HIGHLIGHT = (255, 222, 87, 60) 
CROSS_HIGHLIGHT = (69, 132, 182, 60) 
HIGHLIGHT_COLOR = (0, 255, 0, 45) 

highlight_surface = pxl.Surface((SQUARE_SIZE, SQUARE_SIZE), pxl.SRCALPHA)

screen = pxl.display.set_mode((WIDTH, HEIGHT))
pxl.display.set_caption('TIC-TAC-TOE')
screen.fill(BG_COLOR)

class Game:
   def __init__(self, players):
      self.players = players
      self.current_player = players[0]
      self.board = np.zeros((ROWS, COLS))
      self.draw_lines()
      self.game_over = False
      self.winner = 0

   def draw_lines(self):
      # Horizontal lines
      pxl.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
      pxl.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
      
      # Vertical lines
      pxl.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
      pxl.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

   def draw_figures(self):
      for row in range(ROWS):
         for col in range(COLS):
            x = col * SQUARE_SIZE + SPACE
            y = row * SQUARE_SIZE + SPACE
            if self.board[row][col] == 1:
               screen.blit(CIRCLE_IMG, (x, y))
            elif self.board[row][col] == 2:
               screen.blit(CROSS_IMG, (x, y))
   
   def highlight_square(self, tiles):
      if self.winner == 1.0:
         highlight_surface.fill(CIRCLE_HIGHLIGHT)
      elif self.winner == 2.0:
         highlight_surface.fill(CROSS_HIGHLIGHT)
      
      for row, col in tiles:
         x = col * SQUARE_SIZE
         y = row * SQUARE_SIZE
         screen.blit(highlight_surface, (x, y))
      
      self.draw_lines()

   def switch_player(self):
      if self.current_player == self.players[0]:
         self.current_player = self.players[1]
      else:
         self.current_player = self.players[0]

   def make_move(self, move):
      (row, col) = move

      if self.current_player == self.players[0]:
         # print(f"{self.current_player.name} chose ({row, col})")
         self.board[row][col] = 1
      elif self.current_player == self.players[1]:
         # print(f"{self.current_player.name} chose ({row, col})")
         self.board[row][col] = 2

      if self.check_win(self.current_player):
         self.game_over = True
      
      self.switch_player()
      self.draw_figures()
   
   def available_square(self, row, col):
      return self.board[row][col] == 0

   def check_win(self, player):
      # vertical win check
      for col in range(COLS):
         if self.board[0][col] != 0 and self.board[0][col] == self.board[1][col] == self.board[2][col]:
            self.winner = self.board[0][col]
            self.highlight_square([(0, col), (1, col), (2, col)])
            print(f"{player.name} won")
            return True

      # horizontal win check
      for row in range(ROWS):
         if self.board[row][0] != 0 and self.board[row][0] == self.board[row][1] == self.board[row][2]:
            self.winner = self.board[row][0]
            self.highlight_square([(row, 0), (row, 1), (row, 2)])
            print(f"{player.name} won")
            return True

      # asc diagonal win check
      if self.board[2][0] != 0 and self.board[2][0] == self.board[1][1] == self.board[0][2]:
         self.winner =  self.board[2][0]
         self.highlight_square([(2, 0), (1, 1), (0, 2)])
         print(f"{player.name} won")
         return True

      # desc diagonal win chek
      if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
         self.winner =  self.board[0][0]
         self.highlight_square([(0, 0), (1, 1), (2, 2)])
         print(f"{player.name} won")
         return True
      
      if 0 not in self.board:
         self.winner = 0
         print("It's a tie.")
         return True
      
      return False
   
   def restart(self):
      screen.fill( BG_COLOR )
      self.draw_lines()
      self.current_player = self.players[0]
      self.board = np.zeros((ROWS, COLS))
      self.draw_lines()
      self.game_over = False
      self.winner = 0

# ? Exploration_Rate => epsilon 

class Player:
   def __init__(self, name, strategy, epsilon):
      self.name = name
      self.strategy = strategy
      self.epsilon = epsilon
      with open('model-2.O.pkl', 'rb') as f:
         self.q_table = pickle.load(f)
      # for state, q_values in self.q_table.items():
      #    print(state, q_values)
      self.states = []

   def available_square(self, board, row, col):
      return board[row][col] == 0
   
   def get_valid_moves(self, board):
      valid_moves = []
      for x in range(3):
         for y in range(3):
            if board[x][y] == 0:
               valid_moves.append((x, y))
      
      return valid_moves

   def update_q_table(self, reward):
      for (state, action_index) in self.states:
         self.q_table[state][action_index] += reward
      
      self.states.clear()

# * Main functions
def main():
   player1 = Player("Human", "Agent", 0.00) # O
   player2 = Player("Agent", "Human", 0.00) # X
   players = [player1, player2]

   game = Game(players)

   running = True
   while running:
      for event in pxl.event.get():

         if event.type == pxl.QUIT:
            print("Game exited.")
            running = False
         
         if event.type == pxl.KEYDOWN and event.key == pxl.K_r:
            # if (game.winner == 1):
            #    print("Human won")
            #    if (player1.strategy == "Agent"):
            #       player1.update_q_table(1)
            #    if (player2.strategy == "Agent"):
            #       player2.update_q_table(-5)
            #       print("Agent learned")

            # elif (game.winner == 2):
            #    print("Agent won")
            #    if (player1.strategy == "Agent"):
            #       player1.update_q_table(-1)
            #    if (player2.strategy == "Agent"):
            #       player2.update_q_table(1)
            #       print("Agent learned")

            # else:
            #    if (player1.strategy == "Agent"):
            #       player1.update_q_table(0.5)
            #    if (player2.strategy == "Agent"):
            #       player2.update_q_table(0.5)
            
            game.restart()
         
         if not game.game_over:

            # * Human Moves   
            if game.current_player.strategy == "Human":
               if event.type == pxl.MOUSEBUTTONDOWN:
                  mouseX = event.pos[0]
                  mouseY = event.pos[1]

                  clicked_row = int(mouseY // SQUARE_SIZE)
                  clicked_column = int(mouseX // SQUARE_SIZE)

                  if game.available_square(clicked_row, clicked_column):
                     move = (clicked_row, clicked_column)
                     game.make_move(move)
                  
            # * Random Moves         
            elif game.current_player.strategy == "Random":
               valid_moves = game.current_player.get_valid_moves(game.board)
               move = random.choice(valid_moves)
               game.make_move(move)
            
            # * Agent Moves
            elif game.current_player.strategy == "Agent":
               valid_moves = game.current_player.get_valid_moves(game.board)
               state = tuple(int(x) for x in game.board.flatten())
               # print(state)
               move_index = 0

               if (state not in game.current_player.q_table):
                  # print("Agent: Not in Q-Table")
                  game.current_player.q_table[state] = [0 for x in range(len(valid_moves))]
               
               if (random.random() < game.current_player.epsilon):
                  # print("Agent: Going Random")
                  move_index = random.randint(0, len(valid_moves)-1)
                  move = valid_moves[move_index]
               else:
                  # print("Agent: About to pull up Q-Table")
                  # print(game.current_player.q_table[state])
                  move_index = np.argmax(game.current_player.q_table[state])
                  move = valid_moves[move_index]
               
               game.current_player.states.append((state, move_index))
               game.make_move(move)
      
      pxl.display.update()

   
   # with open('ten-modified-5.x.7x.pkl', 'wb') as f:
   #    pickle.dump(player2.q_table, f)
   
   pxl.quit()
   exit()

main()