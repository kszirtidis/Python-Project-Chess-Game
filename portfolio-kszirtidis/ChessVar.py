# Author: Kayo Zirtidis
# GitHub username: kszirtidis
# Date: 08/10/2023
# Description: Creates a game that is a variant of chess.


class ChessVar:
    """Creates a chess game variant object."""

    def __init__(self):
        """Initializes the chess game."""

        self._chess_board = {"a1": "K", "b1": "B", "c1": "N", "d1": "", "e1": "", "f1": "n", "g1": "b", "h1": "k",
                             "a2": "R", "b2": "B", "c2": "N", "d2": "", "e2": "", "f2": "n", "g2": "b", "h2": "r",
                             "a3": "", "b3": "", "c3": "", "d3": "", "e3": "", "f3": "", "g3": "", "h3": "",
                             "a4": "", "b4": "", "c4": "", "d4": "", "e4": "", "f4": "", "g4": "", "h4": "",
                             "a5": "", "b5": "", "c5": "", "d5": "", "e5": "", "f5": "", "g5": "", "h5": "",
                             "a6": "", "b6": "", "c6": "", "d6": "", "e6": "", "f6": "", "g6": "", "h6": "",
                             "a7": "", "b7": "", "c7": "", "d7": "", "e7": "", "f7": "", "g7": "", "h7": "",
                             "a8": "", "b8": "", "c8": "", "d8": "", "e8": "", "f8": "", "g8": "", "h8": "",
                             }

        self._turn = "white"
        self._game_state = "UNFINISHED"
        self._white_king_reached_row_8 = None

    def make_move(self, move_from, move_to):
        """Moves chess piece from initial square to next position user decides."""

        piece = self._chess_board.get(move_from)

        # Checks if game is correct to start and continue.
        if self._turn == "white" and piece.islower() or self._turn == "black" and piece.isupper():
            return False

        # Does not allow empty spaces to make a move.
        if self._chess_board[move_from] == "":
            return False

        # Allows black and white capture by opposing pieces. Returns False if same color capture.
        if self._turn == "white" and piece.isupper() and self._chess_board[move_to].isupper():
            return False
        elif self._turn == "black" and piece.islower() and self._chess_board[move_to].islower():
            return False

        previous_board_state = self._chess_board.copy()

        # Perform make move
        move_result = self.valid_moves(piece, move_from, move_to)

        # If the move was successful, check if the king is in check.
        if move_result:
            if self.is_king_in_check():
                # The king is in check, so undo the move and return False.
                self._chess_board = previous_board_state
                return False

            if self._game_state == "UNFINISHED" and self._turn == "white":
                self._white_king_reached_row_8 = False

            self.win()  # Calls win method.
            return move_result

        return self.valid_moves(piece, move_from, move_to)

    def valid_moves(self, piece, move_from, move_to):
        """Validates each pieces move for legality."""
        # Checks if piece is a knight.
        if piece in "Nn":

            for knight in ChessVar.get_board(self).keys():
                column_from = ord(move_from[:1])
                row_from = int(move_from[1:])

                column_to = ord(move_to[:1])
                row_to = int(move_to[1:])

                row_diff = abs(row_from - row_to)
                col_diff = abs(column_from - column_to)

                if row_diff == 1 and col_diff == 2 or row_diff == 2 and col_diff == 1:

                    # Moves piece.
                    self._chess_board[move_to] = self._chess_board[move_from]
                    self._chess_board[move_from] = ""

                    # Changes turn.
                    self._turn = "white" if self._turn == "black" else "black"
                    return True
                else:
                    return False

        # Checks if piece is a bishop.
        if piece in "Bb":

            for bishop in ChessVar.get_board(self).keys():
                column_from = ord(move_from[:1])
                row_from = int(move_from[1:])

                column_to = ord(move_to[:1])
                row_to = int(move_to[1:])

                row_diff = abs(row_from - row_to)
                col_diff = abs(column_from - column_to)

                if row_diff != col_diff:
                    return False

                from_col, from_row = ord(move_from[0]) - ord('a'), int(move_from[1]) - 1
                to_col, to_row = ord(move_to[0]) - ord('a'), int(move_to[1]) - 1

                col_diff = to_col - from_col
                row_diff = to_row - from_row

                col_step = 1 if col_diff > 0 else -1 if col_diff < 0 else 0
                row_step = 1 if row_diff > 0 else -1 if row_diff < 0 else 0

                current_col = from_col + col_step
                current_row = from_row + row_step

                while current_col != to_col or current_row != to_row:
                    square = chr(current_col + ord('a')) + str(current_row + 1)
                    if self._chess_board[square]:
                        return False
                    current_col += col_step
                    current_row += row_step

                # Moves piece.
                self._chess_board[move_to] = self._chess_board[move_from]
                self._chess_board[move_from] = ""

                # Changes turn.
                self._turn = "white" if self._turn == "black" else "black"
                return True

        # Checks if piece is a rook ,
        if piece in "Rr":

            for rook in ChessVar.get_board(self).keys():
                column_from = ord(move_from[:1])
                row_from = int(move_from[1:])

                column_to = ord(move_to[:1])
                row_to = int(move_to[1:])

                row_diff = abs(row_from - row_to)
                col_diff = abs(column_from - column_to)

                if (row_diff in range(1, 8) and col_diff == 0) or (row_diff == 0 and col_diff in range(1, 8)):

                    from_col, from_row = ord(move_from[0]) - ord('a'), int(move_from[1]) - 1
                    to_col, to_row = ord(move_to[0]) - ord('a'), int(move_to[1]) - 1

                    col_diff = to_col - from_col
                    row_diff = to_row - from_row

                    col_step = 1 if col_diff > 0 else -1 if col_diff < 0 else 0
                    row_step = 1 if row_diff > 0 else -1 if row_diff < 0 else 0

                    current_col = from_col + col_step
                    current_row = from_row + row_step

                    while current_col != to_col or current_row != to_row:
                        square = chr(current_col + ord('a')) + str(current_row + 1)
                        if self._chess_board[square]:
                            return False
                        current_col += col_step
                        current_row += row_step
                else:
                    return False

                # Moves piece.
                self._chess_board[move_to] = self._chess_board[move_from]
                self._chess_board[move_from] = ""

                # Changes turn.
                self._turn = "white" if self._turn == "black" else "black"
                return True

        # Checks if piece is a King.
        if piece in "Kk":

            for king in ChessVar.get_board(self).keys():
                column_from = ord(move_from[:1])
                row_from = int(move_from[1:])

                column_to = ord(move_to[:1])
                row_to = int(move_to[1:])

                row_diff = abs(row_from - row_to)
                col_diff = abs(column_from - column_to)

                if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1) or (row_diff == 1
                                                                                              and col_diff == 1):

                    # Moves piece.
                    self._chess_board[move_to] = self._chess_board[move_from]
                    self._chess_board[move_from] = ""

                    # Changes turn.
                    self._turn = "white" if self._turn == "black" else "black"
                    return True
                else:
                    return False

    def get_game_state(self):
        """Returns game state"""

        return self._game_state

    def get_board(self):
        """Returns game board."""
        return self._chess_board

    def get_turn(self):
        """Returns turn"""
        return self._turn

    def is_king_in_check(self):
        """Checks if either king is in check and returns True if it is, False otherwise."""

        # Finding the position of both kings.
        white_king_position = None
        black_king_position = None
        for position, piece in self._chess_board.items():
            if piece == "K":
                white_king_position = position
            if piece == "k":
                black_king_position = position

        # Checking if any of the opponent's pieces can attack the king.
        for position, piece in self._chess_board.items():
            if piece and piece.islower():
                if self.valid_moves(piece, position, white_king_position):
                    return True
            if piece and piece.isupper():
                if self.valid_moves(piece, position, black_king_position):
                    return True

        return False

    def win(self):
        """Checks if there is a win or tie."""
        for position, piece in self._chess_board.items():
            if piece == "K" and position[1] == '8' and self._turn == 'white':
                self._game_state = "WHITE_WINS"
            elif piece == "k" and position[1] == '8':
                if self._game_state == "WHITE_WINS":
                    self._game_state = "TIE"
                else:
                    self._game_state = "BLACK_WINS"
