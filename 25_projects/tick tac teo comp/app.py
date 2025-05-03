import math

# Board representation
board = [' ' for _ in range(9)]

def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def available_moves():
    return [i for i, spot in enumerate(board) if spot == ' ']

def make_move(position, player):
    board[position] = player

def is_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_draw():
    return ' ' not in board

def minimax(is_maximizing):
    if is_winner('O'):
        return {'score': 1}
    elif is_winner('X'):
        return {'score': -1}
    elif is_draw():
        return {'score': 0}

    if is_maximizing:
        best = {'score': -math.inf}
        for move in available_moves():
            board[move] = 'O'
            sim_score = minimax(False)
            board[move] = ' '
            sim_score['move'] = move
            if sim_score['score'] > best['score']:
                best = sim_score
        return best
    else:
        best = {'score': math.inf}
        for move in available_moves():
            board[move] = 'X'
            sim_score = minimax(True)
            board[move] = ' '
            sim_score['move'] = move
            if sim_score['score'] < best['score']:
                best = sim_score
        return best

def player_move():
    while True:
        try:
            move = int(input('Enter your move (1-9): ')) - 1
            if move in available_moves():
                make_move(move, 'X')
                break
            else:
                print('Invalid move. Try again.')
        except ValueError:
            print('Please enter a number between 1 and 9.')

def ai_move():
    print('AI is making a move...')
    move = minimax(True)['move']
    make_move(move, 'O')

def main():
    print('Welcome to Tic-Tac-Toe! You are X, AI is O.')
    print_board()
    while True:
        player_move()
        print_board()
        if is_winner('X'):
            print('You win!')
            break
        if is_draw():
            print('It\'s a draw!')
            break
        ai_move()
        print_board()
        if is_winner('O'):
            print('AI wins!')
            break
        if is_draw():
            print('It\'s a draw! ')
            break

if __name__ == '__main__':
    main()
