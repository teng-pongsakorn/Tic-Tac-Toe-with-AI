import random

BLANK = ' '
X = 'X'
O = 'O'

CONTINUE = 'Game not finished'
X_WINS = 'X wins'
O_WINS = 'O wins'
DRAW = 'Draw'

COORD_TO_IDX = {
    (1,3): 0, (2,3): 1, (3,3): 2,
    (1,2): 3, (2,2): 4, (3,2): 5,
    (1,1): 6, (2,1): 7, (3,1): 8
}

WINNING_POSITIONS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]


class CoordinateError(Exception):
    pass


class CellOccupyError(Exception):
    pass


class Player:

    VALID_MOVE = {1, 2, 3}

    def __init__(self, symbol):
        self.symbol = symbol
        self.game = None

    def set_game(self, game):
        self.game = game

    def move(self):
        idx = self.get_next_move()
        self.game.cell_state[idx] = self.symbol

    def get_next_move(self):
        pass

    def get_opponent(self):
        return X if self.symbol == O else O


class User(Player):

    def get_next_move(self):
        while True:
            user_input = input("Enter the coordinates: > ")
            try:
                col, row = map(int, user_input.split())
                if col not in self.VALID_MOVE or row not in self.VALID_MOVE:
                    raise CoordinateError
                idx = COORD_TO_IDX[(col, row)]
                if self.game.cell_state[idx] != BLANK:
                    raise CellOccupyError
                return idx
            except ValueError:
                print("You should enter numbers!")
            except CoordinateError:
                print("Coordinates should be from 1 to 3!")
            except CellOccupyError:
                print('This cell is occupied! Choose another one!')


class AI(Player):

    def __init__(self, symbol, level):
        self.level = level
        super().__init__(symbol)
        if level == 'easy':
            self.get_next_move = self.get_next_move_easy
        elif level == 'medium':
            self.get_next_move = self.get_next_move_medium
        elif level == 'hard':
            self.get_next_move = self.get_next_move_hard

    def get_next_move_easy(self):
        available_idx = [i for i, val in enumerate(self.game.cell_state) if val == BLANK]
        print('Making move level "easy"')
        return random.choice(available_idx)

    def get_next_move_medium(self):
        print('Making move level "medium"')

        # If it already has two in a row and can win with one further move, it does so.
        my_next_winning_move = self.search_next_win(self.symbol)
        if my_next_winning_move is not None:
            return my_next_winning_move

        # If its opponent can win with one move, it plays the move necessary to block this.
        my_mext_losing_move = self.search_next_win(self.get_opponent())
        if my_mext_losing_move is not None:
            return my_mext_losing_move

        # Otherwise, it makes a random move.
        available_idx = [i for i, val in enumerate(self.game.cell_state) if val == BLANK]
        return random.choice(available_idx)

    def search_next_win(self, player):
        for i, j, k in WINNING_POSITIONS:
            if self.game.cell_state[i] == player and self.game.cell_state[j] == player and self.game.cell_state[k] == BLANK:
                return k
            elif self.game.cell_state[j] == player and self.game.cell_state[k] == player and self.game.cell_state[i] == BLANK:
                return i
            elif self.game.cell_state[i] == player and self.game.cell_state[k] == player and self.game.cell_state[j] == BLANK:
                return j
        return None

    def get_next_move_hard(self):
        print('Making move level "hard"')
        best_move = None
        best_score = -100
        for i, val in enumerate(self.game.cell_state):
            if val == BLANK:
                new_board = list(self.game.cell_state)
                new_board[i] = self.symbol
                next_player = self.get_opponent()
                score = minimax(new_board, next_player, maximize=False)
                if score > best_score:
                    best_move = i
                    best_score = score
        return best_move



def minimax(board, player, maximize):

    # base cases: maximize win -> -1, minimize win -> 1, draw -> 0
    prev_player = X if player == O else O
    if TicTacToe.has_winner(board, prev_player):
        return 1 if not maximize else -1
    elif TicTacToe.has_draw(board):
        return 0

    if maximize:
        best_score = -100
        for i, val in enumerate(board):
            if val == BLANK:
                new_board = list(board)
                new_board[i] = player
                score = minimax(new_board, prev_player, not maximize)
                if score > best_score:
                    best_score = score
    else:
        best_score = 100
        for i, val in enumerate(board):
            if val == BLANK:
                new_board = list(board)
                new_board[i] = player
                score = minimax(new_board, prev_player, not maximize)
                if score < best_score:
                    best_score = score
    return best_score




class TicTacToe:

    def __init__(self, first_player, second_player):
        self.X = first_player
        self.O = second_player
        self.X.set_game(self)
        self.O.set_game(self)
        self.cell_state = [BLANK] * 9
        self.game_state = CONTINUE

    def check(self, player):
        if self.has_winner(self.cell_state, player):
            return f'{player} wins'
        elif self.has_draw(self.cell_state):
            return DRAW
        return CONTINUE

    def play(self):
        self.display()
        while True:
            self.X.move()
            self.display()
            self.game_state = self.check(X)
            if self.game_state != CONTINUE:
                print(self.game_state)
                break
            self.O.move()
            self.display()
            self.game_state = self.check(O)
            if self.game_state != CONTINUE:
                print(self.game_state)
                break

    @staticmethod
    def has_winner(cell_state, player):
        for i, j, k in WINNING_POSITIONS:
            if cell_state[i] == player and cell_state[j] == player and cell_state[k] == player:
                return True
        return False

    @staticmethod
    def has_draw(cell_state):
        return cell_state.count(BLANK) == 0

    def display(self):
        print("-" * 9)
        for i in range(0, len(self.cell_state), 3):
            row = self.cell_state[i:i + 3]
            print('|', *row, '|', sep=' ')
        print('-' * 9)


def get_player_from_string(player, symbol):
    if player == 'user':
        return User(symbol=symbol)
    elif player in {'easy', 'medium', 'hard'}:
        return AI(symbol=symbol, level=player)
    else:
        raise ValueError


def get_command():
    while True:
        inp = input("Input command: > ")
        if inp == 'exit':
            return inp
        try:
            start, player1, player2 = inp.split()
            if start != 'start':
                raise ValueError
            first_player = get_player_from_string(player1, X)
            second_player = get_player_from_string(player2, O)
            return first_player, second_player
        except ValueError:
            print("Bad parameters!")


def main():
    while True:
        command = get_command()
        if command == 'exit':
            break
        first_player, second_player = command
        game = TicTacToe(first_player, second_player)
        game.play()


if __name__ == '__main__':
    main()