

import random
import numpy as np
import pickle

COLS, ROWS = 3, 3

class Game:
   def __init__(self, players):
      self.players = players
      self.board = np.zeros((ROWS, COLS))
      self.game_over = False
      self.winner = ""
   
   def play_game(self):
      while True:
         move = self.players[0].make_move(self.board)
         (row, col) = move
         self.board[row][col] = 1
         self.check_win()
         if (self.game_over):
            break
         
         move = self.players[1].make_move(self.board)
         (row, col) = move
         self.board[row][col] = 2
         self.check_win()
         if (self.game_over):
            break

   def check_win(self):
      # vertical win check
      for col in range(COLS):
         if self.board[0][col] != 0 and self.board[0][col] == self.board[1][col] == self.board[2][col]:
            self.winner = self.board[0][col]
            self.game_over = True
            return

      # horizontal win check
      for row in range(ROWS):
         if self.board[row][0] != 0 and self.board[row][0] == self.board[row][1] == self.board[row][2]:
            self.winner = self.board[row][0]
            self.game_over = True
            return

      # asc diagonal win check
      if self.board[2][0] != 0 and self.board[2][0] == self.board[1][1] == self.board[0][2]:
         self.winner =  self.board[2][0]
         self.game_over = True
         return

      # desc diagonal win chek
      if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
         self.winner =  self.board[0][0]
         self.game_over = True
         return
      
      if 0 not in self.board:
         self.winner = 0
         self.game_over = True
         return
      
      return

   def reset(self):
      self.board = np.zeros((ROWS, COLS))
      self.game_over = False
      self.winner = ""

class Player:
   def __init__(self, name, strategy, epsilon):
      self.name = name
      self.strategy = strategy
      self.epsilon = epsilon
      with open('ten-modified-5.1.5x.pkl', 'rb') as f:
         self.q_table = pickle.load(f)
      # self.q_table = {}
      self.states = []

   def update_q_table(self, reward):
      for (state, action_index) in self.states:
         self.q_table[state][action_index] += reward
      
      self.states.clear()

   def make_move(self, board):
      valid_moves = []
      for x in range(ROWS):
         for y in range(COLS):
            if board[x][y] == 0:
               valid_moves.append((x, y))

      if self.strategy == "Human":
         print("Valid moves ", valid_moves)
         print("Enter the row: ", end="")
         row = int(input())
         print("Enter the column: ", end="")
         col = int(input())
         move = (row, col)
         while move not in valid_moves:
            print("Invalid move! Please try again.")
            print("Enter the row: ", end="")
            row = int(input())
            print("Enter the column: ", end="")
            col = int(input())
            move = (row, col)
         
         return move
   
      elif self.strategy == "Random":
         return random.choice(valid_moves)
      
      elif self.strategy == "Agent":
         state = tuple(int(x) for x in board.flatten())
         move_index = 0
         if(state not in self.q_table):
            # print("\nNot in table")
            self.q_table[state] = [0 for x in range(len(valid_moves))]
            # print(board)
            # print(self.q_table[state])
         if(random.random() < self.epsilon):
            # print("\nGoing random bro")
            move_index = random.randint(0, len(valid_moves)-1)
            # print(valid_moves)
            # print(move_index)
            move = valid_moves[move_index]
         else:
            # for state, q_values in player1.q_table.items():
               # print(state, q_values)
            # print("\nAbout to pull up the table")
            move_index = np.argmax(self.q_table[state])
            # print(board)
            # print(self.q_table[state])
            # print(valid_moves)
            # print(move_index)
            # print("\n\n")
            move = valid_moves[move_index]
         self.states.append((state, move_index))
         return move

player1 = Player("Player 1", "Human", 0.60)
player2 = Player("Player 2", "Agent", 0.00)
players = [player1, player2]
game = Game(players)

for x in range(2):
   game.play_game()
   if (game.winner == 1):
      print("Human won")
      if (player1.strategy == "Agent"):
         player1.update_q_table(1)
      if (player2.strategy == "Agent"):
         player2.update_q_table(-10)
         print("Agent learned")

   elif (game.winner == 2):
      print("Agent won")
      if (player1.strategy == "Agent"):
         player1.update_q_table(-1)
      if (player2.strategy == "Agent"):
         player2.update_q_table(1)
         print("Agent learned")

   else:
      if (player1.strategy == "Agent"):
         player1.update_q_table(0.5)
      if (player2.strategy == "Agent"):
         player2.update_q_table(0.5)

   game.reset()

# print("\n\n")
# for state, q_values in player1.q_table.items():
#    print(state, q_values)

# player2.epsilon = 0.00
# game2 = Game(players)
# wins = 0
# losses = 0
# ties = 0

# for x in range(10):
#    game2.play_game()
#    if (game2.winner == 2):
#       wins += 1
#    elif (game2.winner == 1):
#       losses += 1
#    else:
#       ties += 1
#    game2.reset()

should_save = int(input("Did agent learn? - "))
if should_save == 1:
   with open('ten-modified-5.1.6x.pkl', 'wb') as f:
      pickle.dump(player2.q_table, f)

# print("Wins: ", wins)
# print("Losses: ", losses)
# print("Ties: ", ties)

# for x in range(1000):
#    game.play_game()
#    if (game.winner == 1):
#       print("Player 1 wins")
#    elif (game.winner == 2):
#       print("Player 2 wins")
#    else:
#       print("Game Tie")
#    game.reset()


