import curses
import random

#ESTE ALGORITMO UTILIZA O MÉTODO DE BUSCA EM LARGURA MINIMAX


# Movimentos possíveis

MOVIMENTOS = [(0, 0), (0, 1), (0, 2),
         (1, 0), (1, 1), (1, 2),
         (2, 0), (2, 1), (2, 2)]

# POSIÇÕES DOS MOVIMENTOS GANHADORES

MOVIMENTOSGAN = [[(0, 0), (0, 1), (0, 2)],
                 [(1, 0), (1, 1), (1, 2)],
                 [(2, 0), (2, 1), (2, 2)],
                 [(0, 0), (1, 0), (2, 0)],
                 [(0, 1), (1, 1), (2, 1)],
                 [(0, 2), (1, 2), (2, 2)],
                 [(0, 0), (1, 1), (2, 2)],
                 [(0, 2), (1, 1), (2, 0)]]

# Definição dos símbolos para os jogadores
JOGADOR_X = 'X'
JOGADOR_O = 'O'

def start(stdscr):
    stdscr.clear()
    stdscr.addstr("O JOGO COMEÇOU!\n")
    stdscr.refresh()
    curses.napms(1000)

def table(stdscr, board):
    stdscr.clear()
    stdscr.addstr("  1 2 3\n")
    for i in range(3):
        stdscr.addstr(str(i + 1) + ' ')
        for j in range(3):
            stdscr.addstr(board[i][j] + ' ')
        stdscr.addstr('\n')
    stdscr.refresh()

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def done(board):
    # Verificar se há uma vitória
    for move in MOVIMENTOSGAN:
        symbols = [board[x][y] for (x, y) in move]
        if symbols.count(JOGADOR_X) == 3 or symbols.count(JOGADOR_O) == 3:
            return True

    # Verificar se há um empate
    if len(get_available_moves(board)) == 0:
        return True

    return False

def get_winner(board):
    for move in MOVIMENTOSGAN:
        symbols = [board[x][y] for (x, y) in move]
        if symbols.count(JOGADOR_X) == 3:
            return JOGADOR_X
        elif symbols.count(JOGADOR_O) == 3:
            return JOGADOR_O
    return None

def make_move(board, move, player):
    if board[move[0]][move[1]] == ' ':
        board[move[0]][move[1]] = player

def minimax(board, depth, maximizing_player):
    if done(board):
        winner = get_winner(board)
        if winner == JOGADOR_X:
            return 1
        elif winner == JOGADOR_O:
            return -1
        else:
            return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            make_move(board, move, JOGADOR_X)
            eval = minimax(board, depth + 1, False)
            max_eval = max(max_eval, eval)
            board[move[0]][move[1]] = ' '
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            make_move(board, move, JOGADOR_O)
            eval = minimax(board, depth + 1, True)
            min_eval = min(min_eval, eval)
            board[move[0]][move[1]] = ' '
        return min_eval

def find_best_move(board):
    best_eval = float('-inf')
    best_move = None
    for move in get_available_moves(board):
        make_move(board, move, JOGADOR_X)
        eval = minimax(board, 0, False)
        board[move[0]][move[1]] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def BUSCA_EM_LARGURA(stdscr):
    curses.curs_set(0)
    start(stdscr)

    while True:
        # Randomizar quem inicia o jogo
        players = [JOGADOR_X, JOGADOR_O]
        random.shuffle(players)
        current_player = players[0]

        board = [[' ' for _ in range(3)] for _ in range(3)]

        table(stdscr, board)

        while not done(board):
            if current_player == JOGADOR_X:
                move = find_best_move(board)
                make_move(board, move, current_player)
            else:
                stdscr.addstr("Sua vez (linha coluna): ")
                stdscr.refresh()
                user_input = stdscr.getstr().decode()
                move = tuple(map(int, user_input.split()))
                make_move(board, move, current_player)

            table(stdscr, board)
            current_player = JOGADOR_X if current_player == JOGADOR_O else JOGADOR_O

        winner = get_winner(board)
        if winner:
            stdscr.addstr("O jogador " + winner + " venceu!\n")
        else:
            stdscr.addstr("O jogo empatou!\n")

        stdscr.addstr("Deseja jogar novamente? (s/n): ")
        stdscr.refresh()
        user_input = stdscr.getstr().decode()
        if user_input.lower() != 's':
            break

if __name__ == '__main__':
    curses.wrapper(BUSCA_EM_LARGURA)