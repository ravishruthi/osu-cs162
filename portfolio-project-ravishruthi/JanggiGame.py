# Author: Shruthi Ravi
# Date: 03/11/2021
# Description: A program that allows for the user to play an abstract game of Janggi.
#

import copy


class Piece:
    """
        Represents a playing piece for the game.
        The Square class will communicate with this class.
    """
    def __init__(self, side):
        """
            Initializes a Piece object with side (either 'blue' or 'red'),
            whether it has been captured or not and whether if moved, it will
            place the General piece in check.
        :param side: the player color
        """
        self._side = side
        self._is_captured = False
        self._in_check = False

    def set_is_captured(self, boolean):
        self._is_captured = boolean

    def get_is_captured(self):
        return self._is_captured

    def get_side(self):
        return self._side

    def legal_move(self, start_sq, end_sq, board):
        """Checks whether the move is legal for the Piece."""
        pass

    def is_checked(self, start_sq, end_sq, board):
        """
            Checks to see whether the moving of the Piece object place
            the General piece for the player in check.
        """
        pass


class General(Piece):
    """
        Inherits from Piece and represents a General Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a General Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the General. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # get palace details
        if self._side == "red":
            palace = board.get_red_palace()
        else:
            palace = board.get_blue_palace()
        # Get the Square object for start and end locations
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)

        # move only in palace
        if end_sq not in palace:
            return False

        # moves only one space at a time
        if abs(end_sq.get_row() - start_sq.get_row()) > 1 or abs(end_sq.get_col() - start_sq.get_col()) > 1:
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        # otherwise move is good
        return True

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if it will be in check if it moves."""
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if sq.get_piece().get_side() != self._side:
                        if sq.get_piece().legal_move(sq.get_location(), end_sq.get_location(), board):
                            return True
        return False


class Guard(Piece):
    """
        Inherits from Piece and represents a Guard Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Guard Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Guard. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # get palace details
        if self._side == "red":
            palace = board.get_red_palace()
        else:
            palace = board.get_blue_palace()
        # Get the Square object for start and end locations
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)

        # move only in palace
        if end_sq not in palace:
            return False

        # moves only one space at a time
        if abs(end_sq.get_row() - start_sq.get_row()) > 1 or abs(end_sq.get_col() - start_sq.get_col()) > 1:
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        # otherwise move is good
        return True

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Horse(Piece):
    """
        Inherits from Piece and represents a Horse Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Horse Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Horse. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # Get the Square object for start and end locations
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)

        # is end square legal?
        possible_end_squares = self._possible_moves(start_sq, board)
        if end_sq not in possible_end_squares:
            return False
        # Again, illegal move
        if abs(start_sq.get_row() - end_sq.get_row()) > 2 or abs(start_sq.get_row() - end_sq.get_row()) < 1:
            return False
        if abs(start_sq.get_col() - end_sq.get_col()) > 2 or abs(start_sq.get_col() - end_sq.get_col()) < 1:
            return False

        # is it blocked?
        if self._is_blocked(start_sq, end_sq, board):
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        # move is good
        return True

    def _possible_moves(self, start_sq, board):
        """
            Check to see the possible squares that the Horse could move to
            in regards to its rules.
        :param start_sq: Starting Square, or Square object it is currently on
        :param board: The board object for the Janggi Game
        :return: A list of squares that it can legally move to
        """
        game_board = board.get_board()
        current_sq_row = start_sq.get_row()
        current_sq_col = start_sq.get_col()
        legal_end_squares = []
        try:
            legal_end_squares.append(game_board[current_sq_row - 1][current_sq_col - 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 1][current_sq_col - 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 2][current_sq_col - 1])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 2][current_sq_col + 1])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 1][current_sq_col + 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 1][current_sq_col + 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 2][current_sq_col - 1])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 2][current_sq_col + 1])
        except IndexError:
            pass
        return legal_end_squares

    def _is_blocked(self, start_sq, end_sq, board):
        """
            Checks to see if there is a Piece blocking its path to the End Square.
        :param start_sq: Starting Square, or current Square object it is "on"
        :param end_sq: Ending Square, or the Square object it wants to move to.
        :param board: The board object for the Janggi Game
        :return: True if it is being blocked, False if not.
        """
        game_board = board.get_board()
        current_sq_row = start_sq.get_row()
        current_sq_col = start_sq.get_col()
        end_sq_row = end_sq.get_row()
        end_sq_col = end_sq.get_col()
        if current_sq_row - 2 == end_sq_row:
            # check top square
            if game_board[current_sq_row - 1][current_sq_col].get_piece() is not None:
                return True
        elif current_sq_row + 2 == end_sq_row:
            # check bottom square
            if game_board[current_sq_row + 1][current_sq_col].get_piece() is not None:
                return True
        elif current_sq_col + 2 == end_sq_col:
            # check right square
            if game_board[current_sq_row][current_sq_col + 2].get_piece() is not None:
                return True
        elif current_sq_col - 2 == end_sq_col:
            # check left square
            if game_board[current_sq_row][current_sq_col - 2].get_piece() is not None:
                return True
        return False

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Elephant(Piece):
    """
        Inherits from Piece and represents a Elephant Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Elephant Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Elephant. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # Get the Square object for start and end locations
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)

        # is end square legal?
        possible_end_squares = self._possible_moves(start_sq, board)
        if end_sq not in possible_end_squares:
            return False
        # Again, illegal move
        if abs(start_sq.get_row() - end_sq.get_row()) > 3 or abs(start_sq.get_row() - end_sq.get_row()) < 2:
            return False
        if abs(start_sq.get_col() - end_sq.get_col()) > 3 or abs(start_sq.get_col() - end_sq.get_col()) < 2:
            return False

        # is it blocked?
        if self._is_blocked(start_sq, end_sq, board):
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        # move is good
        return True

    def _possible_moves(self, start_sq, board):
        """
            Check to see the possible squares that the Elephant could move to
            in regards to its rules.
        :param start_sq: Starting Square, or Square object it is currently on
        :param board: The board object for the Janggi Game
        :return: A list of squares that it can legally move to
        """
        game_board = board.get_board()
        current_sq_row = start_sq.get_row()
        current_sq_col = start_sq.get_col()
        legal_end_squares = []
        try:
            legal_end_squares.append(game_board[current_sq_row - 2][current_sq_col - 3])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 2][current_sq_col - 3])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 3][current_sq_col - 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 3][current_sq_col + 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row - 2][current_sq_col + 3])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 2][current_sq_col + 3])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 3][current_sq_col - 2])
        except IndexError:
            pass
        try:
            legal_end_squares.append(game_board[current_sq_row + 3][current_sq_col + 2])
        except IndexError:
            pass
        return legal_end_squares

    def _is_blocked(self, start_sq, end_sq, board):
        """
            Checks to see if there is a Piece blocking its path to the End Square.
        :param start_sq: Starting Square, or current Square object it is "on"
        :param end_sq: Ending Square, or the Square object it wants to move to.
        :param board: The board object for the Janggi Game
        :return: True if it is being blocked, False if not.
        """
        game_board = board.get_board()
        current_sq_row = start_sq.get_row()
        current_sq_col = start_sq.get_col()
        end_sq_row = end_sq.get_row()
        end_sq_col = end_sq.get_col()

        if current_sq_row - 3 == end_sq_row:
            # top
            if game_board[current_sq_row - 1][current_sq_col].get_piece() is not None:
                return True
            elif current_sq_col < end_sq_col:
                if game_board[current_sq_row - 2][current_sq_col + 1].get_piece() is not None:
                    return True
            elif current_sq_col > end_sq_col:
                if game_board[current_sq_row - 2][current_sq_col - 1].get_piece() is not None:
                    return True
        elif current_sq_row + 3 == end_sq_row:
            # bottom
            if game_board[current_sq_row + 1][current_sq_col].get_piece() is not None:
                return True
            elif current_sq_col < end_sq_col:
                if game_board[current_sq_row + 2][current_sq_col + 1].get_piece() is not None:
                    return True
            elif current_sq_col > end_sq_col:
                if game_board[current_sq_row + 2][current_sq_col - 1].get_piece() is not None:
                    return True
        elif current_sq_col + 3 == end_sq_col:
            # right
            if game_board[current_sq_row][current_sq_col + 1].get_piece() is not None:
                return True
            elif current_sq_row < end_sq_row:
                if game_board[current_sq_row + 1][current_sq_col + 2].get_piece() is not None:
                    return True
                pass
            elif current_sq_row > end_sq_row:
                if game_board[current_sq_row - 1][current_sq_col + 2].get_piece() is not None:
                    return True
        elif current_sq_col - 3 == end_sq_col:
            # left
            if game_board[current_sq_row][current_sq_col - 1].get_piece() is not None:
                return True
            elif current_sq_row < end_sq_row:
                if game_board[current_sq_row + 1][current_sq_col - 2].get_piece() is not None:
                    return True
                pass
            elif current_sq_row > end_sq_row:
                if game_board[current_sq_row - 1][current_sq_col - 2].get_piece() is not None:
                    return True
        return False

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Chariot(Piece):
    """
        Inherits from Piece and represents a Chariot Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Chariot Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Chariot. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # get palace details
        if self._side == "red":
            palace = board.get_red_palace()
        else:
            palace = board.get_blue_palace()
        # get squares
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)
        # get row and col for start and end square
        start_row = start_sq.get_row()
        start_col = start_sq.get_col()
        end_row = end_sq.get_row()
        end_col = end_sq.get_col()

        # if moving diagonal and not in palace, return False
        if abs(start_row - end_row) == abs(start_col - end_col) and start_sq not in palace and end_sq not in palace:
            return False
        # not moving vertically or horizontally
        elif not (start_sq.get_row() != end_sq.get_row() and start_sq.get_col() == end_sq.get_col()) \
                and not (start_sq.get_row() == end_sq.get_row() and start_sq.get_col() != end_sq.get_col()):
            return False
        # Will technically be considered "blocked" if there is another Piece in between the start and end
        if self._is_blocked(start_sq, end_sq, board):
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        # move is good
        return True

    def _is_blocked(self, start_sq, end_sq, board):
        """
            Checks to see if there is a Piece blocking its path to the End Square.
        :param start_sq: Starting Square, or current Square object it is "on"
        :param end_sq: Ending Square, or the Square object it wants to move to.
        :param board: The board object for the Janggi Game
        :return: True if it is being blocked, False if not.
        """
        current_sq_row = start_sq.get_row()
        current_sq_col = start_sq.get_col()
        end_sq_row = end_sq.get_row()
        end_sq_col = end_sq.get_col()

        if current_sq_row == end_sq_row:
            squares_in_row = board.get_board()[current_sq_row]
            for square in squares_in_row:
                if current_sq_col < square.get_col() < end_sq_col:
                    if square.get_piece() is not None:
                        return True
                elif current_sq_col > square.get_col() > end_sq_col:
                    if square.get_piece() is not None:
                        return True
        elif current_sq_col == end_sq_col:
            squares_in_col = []
            for sq_list in board.get_board():
                for square in sq_list:
                    if square.get_col() == current_sq_col:
                        squares_in_col.append(square)
            for square in squares_in_col:
                if current_sq_row < square.get_row() < end_sq_row:
                    if square.get_piece() is not None:
                        return True
                elif current_sq_row > square.get_row() > end_sq_row:
                    if square.get_piece() is not None:
                        return True
        elif abs(current_sq_row - end_sq_row) == abs(current_sq_col - end_sq_col):
            if end_sq in board.get_red_palace():
                if board.get_board()[1][4].get_piece() is not None:
                    return True
            if end_sq in board.get_blue_palace():
                if board.get_board()[8][4].get_piece() is not None:
                    return True
        return False

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Cannon(Piece):
    """
        Inherits from Piece and represents a Cannon Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Cannon Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Cannon. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # get squares
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)
        # get row and col for start and end square
        start_row = start_sq.get_row()
        start_col = start_sq.get_col()
        end_row = end_sq.get_row()
        end_col = end_sq.get_col()
        # get palace details
        palace = None
        if end_row == 0 or end_row == 1 or end_row == 2:
            palace = board.get_red_palace()
        elif end_row == 7 or end_row == 8 or end_row == 9:
            palace = board.get_blue_palace()
        elif self._side == "red":
            palace = board.get_red_palace()
        else:
            palace = board.get_blue_palace()

        # if moving diagonal and not in palace, return False
        if abs(start_row - end_row) == abs(start_col - end_col) \
                and start_sq not in palace and end_sq not in palace:
            return False
        # if diagonal and in palace, consider it legal
        if abs(start_row - end_row) == abs(start_col - end_col):
            pass
        # not moving vertically or horizontally
        elif not (start_sq.get_row() != end_sq.get_row() and start_sq.get_col() == end_sq.get_col()) \
             and not (start_sq.get_row() == end_sq.get_row() and start_sq.get_col() != end_sq.get_col()):
            return False
        # check if exactly one piece in between
        if not self._is_one_piece_between(start_row, start_col, end_row, end_col, board, palace):
            return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        return True

    def _is_one_piece_between(self, s_row, s_col, e_row, e_col, board, palace):
        """
            Checks to see that there is exactly one object in between the start and
            end location of Cannon, and that the screen object is not a Cannon.
        :param s_row: Start location row
        :param s_col: Start location column
        :param e_row: End location row
        :param e_col: End location column
        :param board: The board object for the Janggi Game
        :param palace: The palace of side player is on, None if not
        :return: True if it is being blocked, False if not.
        """
        piece_count = 0
        cannon_type = Cannon(self.get_side())
        # If moving horizontally
        if s_row == e_row:
            sq_list = board.get_board()[s_row]
            for square in sq_list:
                if (s_col < square.get_col() < e_col) or (s_col > square.get_col() > e_col):
                    if square.get_piece() is not None and type(square.get_piece()) != type(cannon_type):
                        piece_count += 1
                    elif square.get_piece() is not None and type(square.get_piece()) == type(cannon_type):
                        return False
        # If moving vertically
        elif s_col == e_col:
            col_list = []
            for sq_list in board.get_board():
                for square in sq_list:
                    if square.get_col() == s_col:
                        col_list.append(square)
            for square in col_list:
                if (s_row < square.get_row() < e_row) or (s_row > square.get_row() > e_row):
                    if square.get_piece() is not None and type(square.get_piece()) != type(cannon_type):
                        piece_count += 1
                    elif square.get_piece() is not None and type(square.get_piece()) == type(cannon_type):
                        return False
        # If moving diagonally and in palace
        elif palace is not None and s_row in palace and e_row in palace:
            if s_row == 0 or s_row == 1 or s_row == 2:
                if board.get_board()[1][4].get_piece() is None \
                        or type(board.get_board()[1][4].get_piece()) == type(cannon_type):
                    return False
                piece_count += 1
            if s_row == 7 or s_row == 8 or s_row == 9:
                if board.get_board()[8][4].get_piece() is None \
                        or type(board.get_board()[8][4].get_piece()) == type(cannon_type):
                    return False
                piece_count += 1
        # If more than one object in between or none, not legal
        if piece_count > 1 or piece_count == 0:
            return False
        return True

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Soldier(Piece):
    """
        Inherits from Piece and represents a Cannon Piece.
        ** Refer to Piece **
    """
    def __init__(self, side):
        """
            Initializes a Cannon Piece object.
            ** Refer to Piece **
        """
        super().__init__(side)

    def legal_move(self, start_loc, end_loc, board):
        """
            Checks to see if move is legal and follows the rules specific
            to the Cannon. Returns True, if legal. False if not.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending Location ("algebraic notation")
        :param board: The board object for the Janggi Game
        :return: True if move is legal, False if not
        """
        # get squares
        start_sq = board.get_square_with_loc(start_loc)
        end_sq = board.get_square_with_loc(end_loc)
        # get row and col for start and end square
        start_row = start_sq.get_row()
        start_col = start_sq.get_col()
        end_row = end_sq.get_row()
        end_col = end_sq.get_col()

        # get palace details
        palace = None
        if end_row == 0 or end_row == 1 or end_row == 2:
            palace = board.get_red_palace()
        elif end_row == 7 or end_row == 8 or end_row == 9:
            palace = board.get_blue_palace()
        # Checks legal moves for soldiers moving from red side
        if self._side == "red":
            if end_row - start_row == 1 and end_col == start_col:
                pass
            elif abs(end_col - start_col) == 1 and end_row == start_row:
                pass
            elif start_sq in palace and end_sq in palace:
                if end_row - start_row == 1 and abs(end_col - start_col) == 1:
                    pass
            else:
                return False
        # Checks legal moves for soldiers moving from blue side
        else:
            if end_row - start_row == -1 and end_col == start_col:
                pass
            elif abs(end_col - start_col) == 1 and end_row == start_row:
                pass
            elif start_sq in palace and end_sq in palace:
                if end_row - start_row == -1 and abs(end_col - start_col) == 1:
                    pass
            else:
                return False
        # Check to see if end location has a piece from the player's side
        if end_sq.get_piece() is not None:
            if end_sq.get_piece().get_side() == self._side:
                return False

        # will move cause general to be in check?
        self._in_check = self.is_checked(start_sq, end_sq, board)
        if self._in_check:
            return False
        return True

    def is_checked(self, start_sq, end_sq, board):
        """Will check to see if the General Piece will be in check if it moves."""
        gen_type = General(self.get_side())
        potential_board = copy.deepcopy(board)
        for sq_list in board.get_board():
            for sq in sq_list:
                if sq.get_piece() is not None:
                    if type(sq.get_piece()) == type(gen_type) and sq.get_piece().get_side() == self._side:
                        gen_sq = sq
                        potential_board.get_board()[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
                        potential_board.get_board()[start_sq.get_row()][start_sq.get_col()].set_piece(None)
                        if gen_sq.get_piece().is_checked(gen_sq, gen_sq, potential_board):
                            return True
                        return False


class Square:
    """
        Represents a Square on a Board for the Game.
        The Board class will communicate with this class.
        The Piece class will be communicated with by this class.
    """
    def __init__(self, row, col, piece, location):
        """
            Initializes a Square object with a row, column, Piece object (if
            any, None if not) and location ("algebraic notation").
            This will represent a spot on the board.
        :param row: Row on board
        :param col: Column on board
        :param piece: Piece object currently on this Square, None otherwise
        :param location: The designated "algebraic notation" representing this spot
        """
        self._row = row
        self._col = col
        self._piece = piece
        self._location = location

    def set_piece(self, piece):
        """Sets a Piece object on the Square"""
        self._piece = piece

    def get_piece(self):
        """Returns the Piece object on the Square"""
        return self._piece

    def get_location(self):
        """Returns the location, in algebraic notation, of Square"""
        return self._location

    def get_row(self):
        """Returns the row."""
        return self._row

    def get_col(self):
        """Returns the column"""
        return self._col


class Board:
    """
        Represents a Board for the Game.
        The Game class will communicate with this class.
        The Square class will be communicated with by this class.
    """
    def __init__(self):
        """
            Initializes a Board object with a lists of list of Squares, with the
            Piece objects placed on its initial Squares. It also initializes
            the Squares in the Red Palace and Blue Palace.
        """
        self._squares = [
            # -----------------------------------
            [Square(0, 0, Chariot("red"), "a1"), Square(0, 1, Elephant("red"), "b1"), Square(0, 2, Horse("red"), "c1"),
             Square(0, 3, Guard("red"), "d1"), Square(0, 4, None, "e1"), Square(0, 5, Guard("red"), "f1"),
             Square(0, 6, Elephant("red"), "g1"), Square(0, 7, Horse("red"), "h1"), Square(0, 8, Chariot("red"), "i1")],
            # -----------------------------------
            [Square(1, 0, None, "a2"), Square(1, 1, None, "b2"), Square(1, 2, None, "c2"),
             Square(1, 3, None, "d2"), Square(1, 4, General("red"), "e2"), Square(1, 5, None, "f2"),
             Square(1, 6, None, "g2"), Square(1, 7, None, "h2"), Square(1, 8, None, "i2")],
            # -----------------------------------
            [Square(2, 0, None, "a3"), Square(2, 1, Cannon("red"), "b3"), Square(2, 2, None, "c3"),
             Square(2, 3, None, "d3"), Square(2, 4, None, "e3"), Square(2, 5, None, "f3"),
             Square(2, 6, None, "g3"), Square(2, 7, Cannon("red"), "h3"), Square(2, 8, None, "i3")],
            # -----------------------------------
            [Square(3, 0, Soldier("red"), "a4"), Square(3, 1, None, "b4"), Square(3, 2, Soldier("red"), "c4"),
             Square(3, 3, None, "d4"), Square(3, 4, Soldier("red"), "e4"), Square(3, 5, None, "f4"),
             Square(3, 6, Soldier("red"), "g4"), Square(3, 7, None, "h4"), Square(3, 8, Soldier("red"), "i4")],
            # -----------------------------------
            [Square(4, 0, None, "a5"), Square(4, 1, None, "b5"), Square(4, 2, None, "c5"),
             Square(4, 3, None, "d5"), Square(4, 4, None, "e5"), Square(4, 5, None, "f5"),
             Square(4, 6, None, "g5"), Square(4, 7, None, "h5"), Square(4, 8, None, "i5")],
            # -----------------------------------
            [Square(5, 0, None, "a6"), Square(5, 1, None, "b6"), Square(5, 2, None, "c6"),
             Square(5, 3, None, "d6"), Square(5, 4, None, "e6"), Square(5, 5, None, "f6"),
             Square(5, 6, None, "g6"), Square(5, 7, None, "h6"), Square(5, 8, None, "i6")],
            # -----------------------------------
            [Square(6, 0, Soldier("blue"), "a7"), Square(6, 1, None, "b7"), Square(6, 2, Soldier("blue"), "c7"),
             Square(6, 3, None, "d7"), Square(6, 4, Soldier("blue"), "e7"), Square(6, 5, None, "f7"),
             Square(6, 6, Soldier("blue"), "g7"), Square(6, 7, None, "h7"), Square(6, 8, Soldier("blue"), "i7")],
            # -----------------------------------
            [Square(7, 0, None, "a8"), Square(7, 1, Cannon("blue"), "b8"), Square(7, 2, None, "c8"),
             Square(7, 3, None, "d8"), Square(7, 4, None, "e8"), Square(7, 5, None, "f8"),
             Square(7, 6, None, "g8"), Square(7, 7, Cannon("blue"), "h8"), Square(7, 8, None, "i8")],
            # -----------------------------------
            [Square(8, 0, None, "a9"), Square(8, 1, None, "b9"), Square(8, 2, None, "c9"),
             Square(8, 3, None, "d9"), Square(8, 4, General("blue"), "e9"), Square(8, 5, None, "f9"),
             Square(8, 6, None, "g9"), Square(8, 7, None, "h9"), Square(8, 8, None, "i9")],
            # -----------------------------------
            [Square(9, 0, Chariot("blue"), "a10"), Square(9, 1, Elephant("blue"), "b10"),
             Square(9, 2, Horse("blue"), "c10"),
             Square(9, 3, Guard("blue"), "d10"), Square(9, 4, None, "e10"), Square(9, 5, Guard("blue"), "f10"),
             Square(9, 6, Elephant("blue"), "g10"), Square(9, 7, Horse("blue"), "h10"),
             Square(9, 8, Chariot("blue"), "i10")]
        ]
        self._red_palace = [self._squares[0][3], self._squares[0][4], self._squares[0][5],
                            self._squares[1][3], self._squares[1][4], self._squares[1][5],
                            self._squares[2][3], self._squares[2][4], self._squares[2][5]]
        self._blue_palace = [self._squares[7][3], self._squares[7][4], self._squares[7][5],
                             self._squares[8][3], self._squares[8][4], self._squares[8][5],
                             self._squares[9][3], self._squares[9][4], self._squares[9][5]]

    def get_board(self):
        """Returns the Board."""
        return self._squares

    def set_square(self, square):
        """Sets a square in a Board equal to another square"""
        self._squares[square.get_row()][square.get_col()] = square

    def get_red_palace(self):
        """Returns the Red Palace"""
        return self._red_palace

    def get_blue_palace(self):
        """Returns the Blue Palace"""
        return self._blue_palace

    def get_square_with_loc(self, loc):
        """
            Takes a location, in algebraic notation, and returns the
            Square associated with it.
        """
        square = None
        for sq_list in self._squares:
            for sq in sq_list:
                if loc == sq.get_location():
                    square = sq
        return square

    def make_move(self, start_loc, end_loc):
        """
            Moves the Piece from starting location to ending location and
            updates the Board accordingly.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending location ("algebraic notation")
        :return: True if successful, False if not
        """
        start_sq = self.get_square_with_loc(start_loc)
        end_sq = self.get_square_with_loc(end_loc)
        if start_sq.get_piece().legal_move(start_sq.get_location(), end_sq.get_location(), self):
            if end_sq.get_piece() is not None:
                self._squares[end_sq.get_row()][end_sq.get_col()].get_piece().set_is_captured(True)
            self._squares[end_sq.get_row()][end_sq.get_col()].set_piece(start_sq.get_piece())
            self._squares[start_sq.get_row()][start_sq.get_col()].set_piece(None)
            return True
        return False

    def display_board(self):
        """Displays the current content of the Squares on Board"""
        for sq_list in self._squares:
            for square in sq_list:
                print("Location: ", square.get_location(), "Piece: ", square.get_piece())

    def is_checkmate(self, player):
        """
            Checks to see if player is in checkmate.
        :param player: The player ('blue' or 'red')
        :return: True if in checkmate, False if not
        """
        piece_list = [General(player), Guard(player), Elephant(player),
                      Horse(player), Chariot(player), Cannon(player), Soldier(player)]
        for piece in piece_list:
            for sq_list in self._squares:
                for square in sq_list:
                    if square.get_piece() is not None and square.get_piece().get_side() == player \
                            and type(square.get_piece()) == type(piece):
                        start_sq = square
                        for row in self._squares:
                            for col in row:
                                if not square.get_piece().is_checked(start_sq, col, self):
                                    return False
        return True


class JanggiGame:
    """
        Represents a Game of Janggi.
        The Board class will be communicated with this class.
    """
    def __init__(self):
        """
            Initializes a Game object with a Board, the current state of the
            game and the player's who's turn it is.
        """
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._turn = "blue"

    def is_in_check(self, player):
        """
            Well check to see if the player (passed in) is currently
            in check.
        :param player: The player ('blue' or 'red')
        :return: True if so, False if not
        """
        gen_type = General(player)
        for sq_list in self._board.get_board():
            for square in sq_list:
                if square.get_piece() is not None and type(square.get_piece()) == type(gen_type) \
                        and square.get_piece().get_side() == player:
                    if square.get_piece().is_checked(square, square, self._board):
                        return True
                    return False

    def make_move(self, start_loc, end_loc):
        """
            Checks to see if move is legal and updates the Game accordingly.
        :param start_loc: Starting location ("algebraic notation")
        :param end_loc: Ending location ("algebraic notation")
        :return: True if successful, False if not
        """
        # print("Attempting:", start_loc, "->", end_loc)
        start_sq = self._board.get_square_with_loc(start_loc)
        # self._board.display_board()
        # Checks to see if current player is in checkmate
        if self._board.is_checkmate(self._turn):
            if self._turn == "red":
                self._game_state = "BLUE_WON"
            else:
                self._game_state = "RED_WON"
            return False
        if self._game_state != "UNFINISHED":
            return False
        # If not piece in starting location, change turn and return False
        if start_sq.get_piece() is None:
            if self._turn == "blue":
                self._turn = "red"
            else:
                self._turn = "blue"
            return False
        # If wrong player playing, return False
        if start_sq.get_piece().get_side() != self._turn:
            return False
        # If position does not change, take it as a pass
        if start_loc == end_loc:
            if self._turn == "blue":
                self._turn = "red"
            else:
                self._turn = "blue"
            return True
        # If move is legal, great!
        if self._board.make_move(start_loc, end_loc):
            if self._turn == "blue":
                self._turn = "red"
            else:
                self._turn = "blue"
            return True
        # Else, switch turn
        else:
            if self._turn == "blue":
                self._turn = "red"
            else:
                self._turn = "blue"
        return False

    def get_game_state(self):
        """Returns state of the game"""
        return self._game_state

    def get_turn(self):
        """Returns the current player who's turn it is"""
        return self._turn

    def get_board(self):
        """Returns the board"""
        return self._board
