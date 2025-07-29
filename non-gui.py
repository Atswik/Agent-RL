
import random
import numpy as np
import pickle

COLS, ROWS = 3, 3

class Game:
   def __init__(self, players):
      self.players = players
      self.board = [" " for x in range(9)]
      self.game_over = False
      self.winner = ""

   def print_board(self):
      for x in range(3):
         print(" | ", end="")
         for y in range(3):
            print(self.board[x*3+y], end="")
            print(" | ", end="")
         print("\n----------------")
   
   def play_game(self):
      while True:
         move = self.players[0].make_move(self.board)
         self.board[move] = '❌'
         self.checkForWin()
         if (self.game_over):
            break
         move = self.players[1].make_move(self.board)
         self.board[move] = '⭕️'
         self.checkForWin()
         if (self.game_over):
            break

   def checkForWin(self):
      win_conditions = [
         (0, 1, 2), (3, 4, 5), (6, 7, 8),
         (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6)
      ]

      for (i, j, k) in win_conditions:
         if (self.board[i] != " " and self.board[i] == self.board[j] == self.board[k] and self.board):
            self.game_over = True
            if self.board[i] == "❌":
               self.winner = 0
            elif self.board[i] == "⭕️":
               self.winner = 1

      if " " not in self.board:
         self.game_over = True
         self.winner = 2

      return

   def reset(self):
      self.board = [" " for x in range(9)]
      self.game_over = False
      self.winner = ""

class Player:
   def __init__(self, name, strategy, epsilon):
      self.name = name
      self.strategy = strategy
      self.epsilon = epsilon
      self.q_table = {}
      self.states = []

   def update_q_table(self, reward):
      for (state, action_index) in self.states:
         self.q_table[state][action_index] += reward
      
      self.states.clear()

   def make_move(self, board):
      valid_moves = []
      for x in range(len(board)):
         if board[x] == " ":
            valid_moves.append(x)

      if self.strategy == "Human":
         print("Valid moves ", valid_moves)
         print("Enter your placement: ", end="")
         move = int(input())
         while move not in valid_moves:
            print("Invalid move! Please try again.")
            move = int(input())
         return move
   
      elif self.strategy == "Random":
         return random.choice(valid_moves)
      
      elif self.strategy == "Agent":
         state = tuple(board)
         move_index = 0
         if(state not in self.q_table):
            self.q_table[state] = [0 for x in range(len(valid_moves))]
         if(random.random() < self.epsilon):
            move_index = random.randint(0, len(valid_moves)-1)
            move = valid_moves[move_index]
         else:
            move_index = np.argmax(self.q_table[state])
            move = valid_moves[move_index]
         self.states.append((state, move_index))
         return move

player1 = Player("Player 1", "Agent", 0.99)
player2 = Player("Player 2", "Random", 0.99)
players = [player1, player2]
game = Game(players)


for x in range(1000000):
   game.play_game()
   if (game.winner == 0):
      if (player1.strategy == "Agent"):
         player1.update_q_table(1)
      if (player2.strategy == "Agent"):
         player2.update_q_table(-1)
      # print("Player 1 wins")
   elif (game.winner == 1):
      if (player1.strategy == "Agent"):
         player1.update_q_table(-1)
      if (player2.strategy == "Agent"):
         player2.update_q_table(1)
      # print("Player 2 wins")
   else:
      if (player1.strategy == "Agent"):
         player1.update_q_table(0.5)
      if (player2.strategy == "Agent"):
         player2.update_q_table(0.5)
      # print("Game Tie") 

   game.reset()

# print("\n\n")
# for state, q_values in player1.q_table.items():
#    print(state, q_values)

player1.epsilon = 0.00
game2 = Game(players)
wins = 0
losses = 0
ties = 0

for x in range(1000):
   game2.play_game()
   if (game2.winner == 0):
      wins += 1
   elif (game2.winner == 1):
      losses += 1
   else:
      ties += 1
   game2.reset()

# with open('hard_mode.pkl', 'wb') as f:
#    pickle.dump(player1.q_table, f)

print("Wins: ", wins)
print("Losses: ", losses)
print("Ties: ", ties)


# for x in range(100):
#    game.play_game()
#    if (game.winner == 0):
#       print("Player 1 wins")
#    elif (game.winner == 1):
#       print("Player 2 wins")
#    else:
#       print("Game Tie")
#    game.reset()
