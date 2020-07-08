import random
import sys


def init_matrix():  # Sets an initial chart for testing purposes
    while True:
        init_board = input("Enter cells: ").upper().replace('_', ' ')
        list_board = list(init_board)
        if len(list_board) != 9:
            print("Please input only 9 letters!")
            continue
        elif not all(x in 'XO ' for x in list_board):
            print("Please enter only 'x' 'o' or '_'!")
            continue
        break

    i = list_board
    mat_board = []
    for x in range(3, 0, -1):
        mat_board.append([i[x * 3 - 3], i[x * 3 - 2], i[x * 3 - 1]])
    return mat_board


def mat_to_image(board):
    image = '''    ---------
    | {2[0]} {2[1]} {2[2]} |
    | {1[0]} {1[1]} {1[2]} |
    | {0[0]} {0[1]} {0[2]} |
    ---------'''
    image = image.format(*board)
    return image


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def whose_turn(board):  # For setting shape for 2P mode
    x = 0
    o = 0
    for row in board:
        for col in row:
            if col == 'X':
                x += 1
            elif col == 'O':
                o += 1
    if x <= o:
        return 'X'
    return 'O'


def game_state(board):
    contains_empty = not all(col in 'XO' for row in board for col in row)
    for i in range(0, 3, 2):
        if board[i][0] == board[1][1] == board[abs(i-2)][2] != ' ':
            return board[1][1] + " wins"
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][1] + " wins"
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[1][i] + " wins"

    if not contains_empty:
        return "Draw"
    else:
        return "Game not finished"


class Player:
    n_players = 0
    def __init__(self, level):
        self.level = level
        self.shape = ''
        self.n_players += 1

    def make_move(self, board):
        self.shape = whose_turn(board)
        print(mat_to_image(board))

        def move_prediction(temp_board1):
            def score_moves(temp_board3):
                for _ in range(9):
                    temp_board4 = temp_board3[:]
                    if temp_board4[pos // 3][pos % 3] == ' ':
                        temp_board4[pos // 3][pos % 3] = whose_turn(temp_board4)
                        state = game_state(temp_board4)
                        if state.endswith('wins'):
                            if letter != self.shpae:
                                return -10
                            else:
                                return 10
                        elif state == 'Draw':
                            return 0
                        return score_moves(temp_board4)

            max_score = -100000
            for i in range(9):
                temp_board2 = temp_board1[:]
                if temp_board2[i // 3][i % 3] != ' ':
                    continue
                temp_board2[i // 3][i % 3] = whose_turn(temp_board2)
                score = score_moves(temp_board2)
                if score > max_score:
                    max_score = score
                    move_to_make = i
            temp_board1[move_to_make // 3][move_to_make % 3] = whose_turn(temp_board1)
            return temp_board1

        if self.level == 'user':
            while True:
                coord = input("Enter the coordinates: ").split(" ")
                # Error checking for coord input
                try:
                    coord = [int(x) - 1 for x in coord]
                except ValueError:
                    print("You should enter numbers!")
                    continue
                if len(coord) != 2:
                    print("You should only enter 2 values!")
                    continue
                if not all(0 <= x <= 2 for x in coord):
                    print("Coordinates should be from 1 to 3!")
                    continue
                if board[coord[1]][coord[0]] != ' ':
                    print("This cell is occupied! Choose another one!")
                    continue

                board[coord[1]][coord[0]] = self.shape
                print(mat_to_image(board))
                return board
        elif self.level in ['easy', 'medium', 'hard']:
            print('Making move level "' + self.level + '"')
            symbol_list = ['X', 'O'] if self.shape == 'X' else ['O', 'X']
            if self.level in ['medium', 'hard']:
                for letter in symbol_list:
                    for pos in range(9):
                        if board[pos // 3][pos % 3] == ' ':
                            board[pos // 3][pos % 3] = letter
                            if game_state(board).endswith('wins'):
                                if letter != self.shape:
                                    board[pos // 3][pos % 3] = self.shape
                                return board
            if self.level != 'hard':
                while True:
                    coord = [random.randint(0, 2), random.randint(0, 2)]
                    if board[coord[1]][coord[0]] != ' ':
                        continue
                    board[coord[1]][coord[0]] = self.shape
                    print(mat_to_image(board))
                    return board
            else:
                return move_prediction(board)



def main():
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # Initial empty board
    while True:  # Menu loop
        action = input("Input command: ").split(' ')
        if action[0] == 'start':
            if len(action) != 3:
                print("Bad parameters!")
                continue
            for i in range(1, 3):
                if action[i] not in ['user', 'easy', 'medium', 'hard']:
                    print("Bad parameters!")
                    continue
            player1 = Player(action[1])
            player2 = Player(action[2])
            break
        elif action == ['exit']:
            sys.exit()
        else:
            print("Bad parameters!")

    while True:  # Game loop
        board = player1.make_move(board) if whose_turn(board) == 'X'else player2.make_move(board)

        g_state = game_state(board)
        if g_state != "Game not finished":
            print(g_state)
            break



if __name__ == '__main__':
    while True: # Loops program infinitely unless 'exit' from menu
        main()