import colorama, ctypes, os, sys
from colorama import Fore
NUMS = "123456789"
MENU_CHOICES = "12E"

ctypes.windll.kernel32.SetConsoleTitleW(f'Tic-Tac-Toe | made by piombacciaio')

def check_input(move):
  if move in NUMS and move != "": return True
  return False

def check_free(row, col, board):
  if board[row][col] != 0: return False
  return True

def coords(move:int):
  row = int(move/3)
  col = move % 3

  return row,col

def check_draw(board):
  if not any(0 in line for line in board): return True
  return False

def check_win(player, board):
  if check_row(player, board): return True
  if check_col(player, board): return True
  if check_diagonals(player, board): return True
  return False

def check_row(player, board):
  for row in board:
    complete_row = True
    for slot in row:
      if slot != player:
        complete_row = False
        break
    if complete_row: return True
  return False 

def check_col(player, board):
  for col in range(3):
    complete_col = True
    for row in range(3):
      if board[row][col] != player:
        complete_col = False
        break
    if complete_col: return True
  return False

def check_diagonals(player, board):
  if board[0][0] == board[1][1] == board[2][2] == player: return True
  elif board[0][2] == board[1][1] == board[2][0] == player: return True
  else: return False

def update_printed_board(board):
  for row in board:

    for index, cell in enumerate(row):
    
      if index != 2:
        if cell != 0: print(cell + " | ", end="")
        else: print("  | ", end="")
      
      else:
        if cell != 0: print(cell, end="")
        else: print("", end="")

    print()

def minimax(board, depth, maximizingPlayer):
    result = check_win("O", board)
    if result:
        return 1
    result = check_win("X", board)
    if result:
        return -1
    if check_draw(board):
        return 0

    if maximizingPlayer:
        bestVal = -sys.maxsize-1
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = "O"
                    val = minimax(board, depth+1, False)
                    board[row][col] = 0
                    bestVal = max(bestVal, val)
        return bestVal
    else:
        bestVal = sys.maxsize
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = "X"
                    val = minimax(board, depth+1, True)
                    board[row][col] = 0
                    bestVal = min(bestVal, val)
        return bestVal

def findBestMove(board):
    bestVal = -sys.maxsize-1
    bestMove = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                board[row][col] = "O"
                moveVal = minimax(board, 0, False)
                board[row][col] = 0
                if moveVal > bestVal:
                    bestMove = (row, col)
                    bestVal = moveVal
    return bestMove

def main():
  #Main menu
  while True:
    
    board = [[0,0,0], [0,0,0], [0,0,0]] #[[row1], [row2], [row3]]

    multiplayer = True
    print("Choose a game mode:\n"\
          f"[{Fore.GREEN}1{Fore.RESET}] Single player\n"\
          f"[{Fore.GREEN}2{Fore.RESET}] Multi player\n"\
          f"[{Fore.GREEN}E{Fore.RESET}] Exit")
    choice = input(">> ").upper()
    if choice not in MENU_CHOICES:
      print(Fore.YELLOW + "Not a valid choice!\n" + Fore.RESET)
      continue
    
    if choice == "1":
      multiplayer = False

    if choice == "2":
      multiplayer = True

    if choice == "E":
      print(Fore.YELLOW + "Thanks for playing!\nPress [ENTER] to quit" + Fore.RESET)
      input()
      break

    # Actual game
    os.system("cls")
    last_turn = 0
    update_printed_board(board)
    while True:

      player = "X" if last_turn == 0 else "O"

      print(f"Player {player} turn")
      if player == "O" and multiplayer == False:
        row, col = findBestMove(board)
        if not check_free(row,col, board):
          continue
        board[row][col] = player

      else:

        player_move = input("Input a cell number (1-9) >> ")

        if player_move.lower() == "q": 
          print(Fore.YELLOW + "Quitting match!\nPress [ENTER] to go back to main menu" + Fore.RESET)
          input()
          break

        if not check_input(player_move):
          print(Fore.YELLOW + "Not a valid choice!\n" + Fore.RESET)
          continue
        player_move = int(player_move) - 1

        row, col = coords(player_move)
        if not check_free(row,col, board):
          print(Fore.YELLOW + "Cell is already taken!\n" + Fore.RESET)
          continue
      
        board[row][col] = player
      print()
      update_printed_board(board)

      if check_win(player=player, board=board):
        print(Fore.GREEN + f"Player {player} won!" + Fore.RESET)
        input()
        break

      if check_draw(board):
        print(Fore.GREEN + "It is a draw!" + Fore.RESET)
        input()
        break

      last_turn = not last_turn

if __name__ == '__main__': 
  colorama.init()
  main()