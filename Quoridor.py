# Author: Matt Gader
# Date: 8/5/2021
# Description: Class QuoridorGame which allows to players to play a game of Quoridor. After initializing
# a game, two players take turns either moving their pawn on the board or placing fences to obstruct the
# opponent. The object of the game is to reach the opponent's baseline (starting row) first.


class QuoridorGame:

    """
    Represents a QuoridorGame object which is used to play a game of Quoridor with two players.
    A game is initialized with a representation of the board containing two pawns, with player one's
    pawn starting on tile (4, 0) and player two's pawn starting on tile (4, 8). The player's alternate
    turns, which can either move the pawn or place a fence (which obstructs pawn movement). Pawns are
    moved one tile at a time (either horizontally or vertically) unless the opponent's pawn is blocking,
    in which case the move can jump over the opponent's pawn. If a jump is blocked by a fence (and other
    fences aren't obstructing the way), the pawn can move diagonally. Each player has ten fences to place,
    either vertically or horizontally. The game is won when a player's pawn reaches the opponent's baseline
    (their pawn's starting row)
    """

    def __init__(self):
        """
        Initializes a quoridor game with data members to initialize the board,
        keep track of whose turn it is, keep track of where on the board the player's
        pawns are, keep track of how many fences each player has left, and keep track
        of if the game has been won
        """
        self._board = [['+==', '+==', '+==', '+==', '+==', '+==', '+==', '+==', '+==', '+'],
                       ['|  ', '   ', '   ', '   ', ' P1', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '|'],
                       ['+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+  ', '+'],
                       ['|  ', '   ', '   ', '   ', ' P2', '   ', '   ', '   ', '   ', '|'],
                       ['+==', '+==', '+==', '+==', '+==', '+==', '+==', '+==', '+==', '+']]
        self._turn = 1
        self._p1 = (4, 0)
        self._p2 = (4, 8)
        self._player = self._p1
        self._opponent = self._p2
        self._opponent_piece = ' P2'   # necessary?
        self._p1Fences = 10
        self._p2Fences = 10
        self._winner = None

    def print_board(self):
        """
        Prints the board in its current state
        """
        for i in range(0, 19):
            print(self._board[i])

    def move_pawn(self, turn, move):
        """
        Determines whether or not a player's move is valid by
        checking if the move is out of bounds, calling correct_turn
        to determine if the move was made in turn, calling move_direction,
        which return False if the move is invalid and checking if the opponent's
        pawn is already occupying the move position. If the move passes all of
        these checks, valid_move is called to implement the move and check_for_win
        is called to check if the game has been won
        """
        x = move[0]
        y = move[1]
        if x < 0 or x > 8:
            return False
        if y < 0 or y > 8:
            return False
        if self.correct_turn(turn) is False:
            return False
        if self._player == move:
            return False
        if self.move_direction(x, y) is False:
            return False
        if self._opponent_piece in self.pawn_conversion(x, y):
            return False
        else:
            self.valid_move(turn, x, y)
            self.check_for_win(turn, y)
            return True

    def valid_move(self, turn, x, y):
        """
        Implements player's move if it is valid
        """
        if turn == 1:
            x_source = self._p1[0]
            y_source = self._p1[1]
            self._p1 = (x, y)
            self._turn = 2
        else:
            x_source = self._p2[0]
            y_source = self._p2[1]
            self._p2 = (x, y)
            self._turn = 1
        if '|' in self.pawn_conversion(x_source, y_source):
            self.set_board('|  ', x_source, y_source)
        else:
            self.set_board('   ', x_source, y_source)
        if '|' in self.pawn_conversion(x, y):
            if turn == 1:
                self.set_board('|P1', x, y)
            else:
                self.set_board('|P2', x, y)
        else:
            if turn == 1:
                self.set_board(' P1', x, y)
            else:
                self.set_board(' P2', x, y)

    def correct_turn(self, turn):
        """
        Checks if a player's move (pawn move or fence
        placement) is in turn, updating player, opponent,
        and opponent piece data members if it is
        """
        if self._winner is not None:
            return False
        elif turn != self._turn:
            return False
        if turn == 1:
            self._player = self._p1
            self._opponent = self._p2
            self._opponent_piece = 'P2'
        else:
            self._player = self._p2
            self._opponent = self._p1
            self._opponent_piece = 'P1'

    def move_direction(self, x, y):
        """
        Calculates direction of move and calls
        appropriate method to determine if move is valid
        """
        if self._player[0] == x:
            if self.vertical_check(x, y) is False:
                return False
        if self._player[1] == y:
            if self.hor_check(x, y) is False:
                return False
        if abs(self._player[0] - x) == 1 and abs(self._player[1] - y) == 1:
            return self.diagonal_check(x, y)
        if abs(self._player[0] - x) + abs(self._player[1] - y) > 2:
            return False

    def set_board(self, string, x, y):
        """
        Converts move coordinates to properly navigate the board,
        allowing for pawns to be moved and placed correctly
        """
        xp = y * 2 + 1
        yp = x
        self._board[xp][yp] = string

    def pawn_conversion(self, x, y):
        """
        Converts pawn coordinates to
        correctly navigate board
        """
        xp = y * 2 + 1
        yp = x
        return self._board[xp][yp]

    def hor_fence_conversion(self, x, y):
        """
        Converts horizontal fence coordinates
        to correctly navigate board
        """
        xf = y * 2
        yf = x
        return self._board[xf][yf]

    def vert_fence_conversion(self, x, y):
        """
        Converts vertical fence coordinates
        to correctly navigate board
        """
        xf = y * 2 + 1
        yf = x
        return self._board[xf][yf]

    def vertical_check(self, x, y):
        """
        Checks vertical move for validity, sends to
        vert_jump_check if move is more than 1 square
        """
        if abs(self._player[1] - y) > 2:
            return False
        elif abs(self._player[1] - y) == 2:
            if self.vert_jump_check(x, y) is False:
                return False
        elif self._player[1] - y == 1:
            if self.hor_fence_conversion(x, y + 1) == '+==':
                return False
        elif self._player[1] - y == -1:
            if self.hor_fence_conversion(x, y) == '+==':
                return False

    def hor_check(self, x, y):
        """
        Checks horizontal move for validity, sends to
        hor_jump_check if move is more than 1 square
        """
        if abs(self._player[0] - x) > 2:
            return False
        elif abs(self._player[0] - x) == 2:
            if self.hor_jump_check(x, y) is False:
                return False
        elif self._player[0] - x == 1:
            if '|' in self.vert_fence_conversion(x + 1, y):
                return False
        elif self._player[0] - x == -1:
            if '|' in self.vert_fence_conversion(x, y):
                return False

    def vert_jump_check(self, x, y):
        """
        Checks if vertical jump is valid
        """
        if self._player[1] - y == 2:
            if self._opponent_piece not in self.pawn_conversion(x, y + 1):
                return False
            elif self.hor_fence_conversion(x, y + 2) == '+==':
                return False
            elif self.hor_fence_conversion(x, y + 1) == "+==":
                return False
        else:
            if self._opponent_piece not in self.pawn_conversion(x, y - 1):
                return False
            elif self.hor_fence_conversion(x, y - 1) == '+==':
                return False
            elif self.hor_fence_conversion(x, y) == "+==":
                return False

    def hor_jump_check(self, x, y):
        """
        Checks if horizontal jump is valid
        """
        if self._player[0] - x == 2:
            if self._opponent_piece not in self.pawn_conversion(x + 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x + 2, y):
                return False
            elif '|' in self.vert_fence_conversion(x + 1, y):
                return False
        else:
            if self._opponent_piece not in self.pawn_conversion(x - 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x - 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x, y):
                return False

    def diagonal_check(self, x, y):
        """
        Determines direction of diagonal move,
        calling appropriate method to check validity
        """
        if self._player[0] - x == -1:
            if self._player[1] - y == 1:
                if self.up_right_check(x, y) is not True:   # if these calls aren't True, return False
                    return False
        if self._player[0] - x == -1:
            if self._player[1] - y == -1:
                if self.down_right_check(x, y) is not True:
                    return False
        if self._player[0] - x == 1:
            if self._player[1] - y == -1:
                if self.down_left_check(x, y) is not True:
                    return False
        if self._player[0] - x == 1:
            if self._player[1] - y == 1:
                if self.up_left_check(x, y) is not True:
                    return False

    def up_right_check(self, x, y):
        """
        Checks validity of up right move
        """
        if self._opponent_piece in self.pawn_conversion(x - 1, y):
            if self.hor_fence_conversion(x - 1, y) == '+==':
                if self.hor_fence_conversion(x - 1, y + 1) != '+==':
                    if '|' not in self.vert_fence_conversion(x, y):
                        return True
        elif self._opponent_piece in self.pawn_conversion(x, y + 1):
            if '|' in self.vert_fence_conversion(x + 1, y + 1):
                if '|' not in self.vert_fence_conversion(x, y + 1):
                    if self.hor_fence_conversion(x, y + 1) != '+==':
                        return True

    def down_right_check(self, x, y):
        """
        Checks validity of down right move
        """
        if self._opponent_piece in self.pawn_conversion(x, y - 1):
            if '|' in self.vert_fence_conversion(x + 1, y - 1):
                if '|' not in self.vert_fence_conversion(x, y - 1):
                    if self.hor_fence_conversion(x, y) != '+==':
                        return True
        elif self._opponent_piece in self.pawn_conversion(x - 1, y):
            if self.hor_fence_conversion(x - 1, y + 1) == '+==':
                if self.hor_fence_conversion(x - 1, y) != '+==':
                    if '|' not in self.vert_fence_conversion(x, y):
                        return True

    def down_left_check(self, x, y):
        """
        Checks validity of down left move
        """
        if self._opponent_piece in self.pawn_conversion(x + 1, y):
            if self.hor_fence_conversion(x + 1, y + 1) == '+==':
                if self.hor_fence_conversion(x + 1, y) != '+==':
                    if '|' not in self.vert_fence_conversion(x + 1, y):
                        return True
        elif self._opponent_piece in self.pawn_conversion(x, y - 1):
            if '|' in self.vert_fence_conversion(x, y - 1):
                if '|' not in self.vert_fence_conversion(x + 1, y - 1):
                    if self.hor_fence_conversion(x, y) != '+==':
                        return True

    def up_left_check(self, x, y):
        """
        Checks validity of up left move
        """
        if self._opponent_piece in self.pawn_conversion(x, y + 1):
            if '|' in self.vert_fence_conversion(x, y + 1):
                if '|' not in self.vert_fence_conversion(x + 1, y + 1):
                    if self.hor_fence_conversion(x, y + 1) != '+==':
                        return True
        if self._opponent_piece in self.pawn_conversion(x + 1, y):
            if self.hor_fence_conversion(x + 1, y) == '+==':
                if self.hor_fence_conversion(x + 1, y + 1) != '+==':
                    if '|' not in self.vert_fence_conversion(x + 1, y):
                        return True

    def place_fence(self, turn, direction, position):
        """
        Initial fence placement check which calls correct_turn
        to verify move is in turn, calls fences_left to verify
        player has fences left, calls fence_check to check if
        fence placement is valid, and updates player's fence
        count if placement is valid
        """

        if self.correct_turn(turn) is False:
            return False
        elif self.fences_left(turn) is False:
            return False
        elif self.fence_check(direction, position) is False:
            return False
        if turn == 1:
            self._p1Fences -= 1
            self._turn = 2
            return True
        else:
            self._p2Fences -= 1
            self._turn = 1
            return True

    def fences_left(self, turn):
        """
        Checks if player has any fences left to place
        """
        if turn == 1:
            if self._p1Fences == 0:
                return False
        else:
            if self._p2Fences == 0:
                return False

    def fence_check(self, direction, position):
        """
        Checks if a fence already exists
        in position, places fence if not
        """
        x = position[0]
        y = position[1]
        if direction == 'h':
            if self.hor_fence_conversion(x, y) == '+==':
                return False
            else:
                xf = y * 2
                yf = x
                self._board[xf][yf] = '+=='
        if direction == 'v':
            if '|' in self.vert_fence_conversion(x, y):
                return False
            else:
                xf = y * 2 + 1
                yf = x
                if 'P1' in self._board[xf][yf]:
                    self._board[xf][yf] = '|P1'
                elif 'P2' in self._board[xf][yf]:
                    self._board[xf][yf] = '|P2'
                else:
                    self._board[xf][yf] = '|  '

    def check_for_win(self, turn, y):
        """
        Updates winner data member if game has been won
        """
        if turn == 1:
            if y == 8:
                self._winner = 1
        else:
            if y == 0:
                self._winner = 2

    def is_winner(self, player):
        """
        Takes player number as argument,
        returns true if player has won, False otherwise
        """
        if self._winner == player:
            return True
        else:
            return False


def main():
    """
    Tests QuoridorGame by playing a game
    """
    q = QuoridorGame()
    print(q.move_pawn(1, (4, 1)))
    print(q.move_pawn(2, (4, 7)))
    print(q.move_pawn(1, (4, 2)))
    print(q.move_pawn(2, (4, 6)))
    print(q.move_pawn(1, (4, 3)))
    print(q.move_pawn(2, (4, 5)))
    print(q.place_fence(1, 'h', (4, 5)))
    print(q.move_pawn(2, (3, 5)))
    print(q.move_pawn(1, (4, 4)))
    print(q.place_fence(2, 'h', (5, 5)))
    print(q.move_pawn(1, (3, 4)))

    print(q.place_fence(2, 'h', (3, 4)))
    print(q.place_fence(1, 'v', (3, 5)))
    print(q.move_pawn(2, (2, 4)))

    # print(q.move_pawn(2, (3, 3)))
    # print(q.move_pawn(1, (3, 5)))
    # print(q.move_pawn(2, (3, 2)))
    # print(q.move_pawn(1, (3, 6)))
    # print(q.move_pawn(2, (3, 1)))
    # print(q.place_fence(1, 'h', (3, 1)))
    # print(q.move_pawn(2, (4, 1)))
    # print(q.move_pawn(1, (3, 7)))
    # print(q.move_pawn(2, (4, 0)))
    # print(q.is_winner(2))
    # print(q.move_pawn(1, (3, 8)))
    q.print_board()

    # print(q.move_pawn(1, (4, 2)))


if __name__ == '__main__':
    main()
