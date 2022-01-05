# Author: Matt Gader
# Date: 8/12/2021
# Description: Class QuoridorGame which allows two players to play a game of Quoridor. After initializing
# a game, two players take turns either moving their pawn on the board or placing fences to obstruct the
# opponent. The object of the game is to reach the opponent's baseline (starting row) first.

class QuoridorGame:
    """
    This represents a QuoridorGame object which is used to play a game of quoridor with two players.
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
        self._fair_play_board = [[False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ],
                                [False, False, False, False, False, False, False, False, False, ]]
        self._fair_play_board1 = []      # used to check fair play rule
        self._turn = 1                   # initialized to player 1
        self._p1 = (4, 0)
        self._p2 = (4, 8)
        self._player = self._p1
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
        Takes parameters turn and move, determines whether or not a player's
        move is out of bounds, calls correct_turn to determine if the move was
        made in turn, calls move_direction which returns False if the move is
        invalid, and checks if the opponent's pawn is already occupying the move
        position. If the move passes all of these checks, calls valid_move to
        implement the move and calls check_for_win to check if the game has
        been won.Returns False if move is invalid
        """
        x = move[0]
        y = move[1]
        if x < 0 or x > 8:                       # checks for out-of-bounds move
            return False
        if y < 0 or y > 8:
            return False
        if self.correct_turn(turn) is False:     # checks if move is in turn
            return False
        if self._player == move:                 # checks if pawn didn't move
            return False
        if self.move_direction(x, y) is False:   # sends to move_direction to check for valid move
            return False
        if 'P' in self.pawn_conversion(x, y):    # checks if pawn already occupies tile
            return False
        else:
            self.valid_move(turn, x, y)          # handles valid move
            self.check_for_win(turn, y)
            return True

    def valid_move(self, turn, x, y):
        """
        Takes turn, x, and y, implements player's move if it is
        valid by updating data member which holds coordinates
        and updating the board to reflect the move
        """

        # updates player coordinates and turn on valid move
        if turn == 1:
            x_source = self._p1[0]
            y_source = self._p1[1]
            self._p1 = (x, y)
            self._turn = 2
        elif turn == 2:
            x_source = self._p2[0]
            y_source = self._p2[1]
            self._p2 = (x, y)
            self._turn = 1

        # sets board after valid move
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
        Takes turn, checks if a player's move (pawn move or fence
        placement) is in turn, updating player data members if it is
        """
        if self._winner is not None:
            return False
        elif turn != self._turn:
            return False

        # sets player data member if move is in turn
        if turn == 1:
            self._player = self._p1
        else:
            self._player = self._p2

    def move_direction(self, x, y):
        """
        Takes x and y, calculates direction of move, calls appropriate
        method to determine if move is valid, returns False to make_move
        if the move is invalid
        """

        # handles vertical move
        if self._player[0] == x:
            if self.vertical_check(x, y) is False:
                return False

        # handles horizontal move
        if self._player[1] == y:
            if self.hor_check(x, y) is False:
                return False

        # handles diagonal move
        if abs(self._player[0] - x) == 1 and abs(self._player[1] - y) == 1:
            return self.diagonal_check(x, y)

        # handles move that is too large to be a jump or diagonal
        if abs(self._player[0] - x) + abs(self._player[1] - y) > 2:
            return False

    def set_board(self, string, x, y):
        """
        Takes x and y, converts coordinates to properly navigate the board,
        allowing for pawns to be moved and placed correctly
        """
        xp = y * 2 + 1
        yp = x
        self._board[xp][yp] = string

    def pawn_conversion(self, x, y):
        """
        Takes x and y, converts pawn coordinates to
        correctly navigate board
        """
        xp = y * 2 + 1
        yp = x
        return self._board[xp][yp]

    def hor_fence_conversion(self, x, y):
        """
        Takes x and y, converts horizontal fence
        coordinates to correctly navigate board
        """
        xf = y * 2
        yf = x
        return self._board[xf][yf]

    def vert_fence_conversion(self, x, y):
        """
        Takes x and y, converts vertical fence
        coordinates to correctly navigate board
        """
        xf = y * 2 + 1
        yf = x
        return self._board[xf][yf]

    def vertical_check(self, x, y):
        """
        Takes x and y, checks vertical move for validity,
        sends to vert_jump_check if move is more than 1 square,
        returns False to move_direction if move is invalid
        """
        # move invalid if more than 2 tiles
        if abs(self._player[1] - y) > 2:
            return False

        # handles vertical jump
        elif abs(self._player[1] - y) == 2:
            if self.vert_jump_check(x, y) is False:
                return False

        # checks for fences
        elif self._player[1] - y == 1:
            if self.hor_fence_conversion(x, y + 1) == '+==':
                return False
        elif self._player[1] - y == -1:
            if self.hor_fence_conversion(x, y) == '+==':
                return False

    def hor_check(self, x, y):
        """
        Takes x and y, checks horizontal move for validity,
        sends to hor_jump_check if move is more than 1 square,
        returns False to move_direction if move is invalid
        """
        # move invalid if more than 2 tiles
        if abs(self._player[0] - x) > 2:
            return False

        # handles horizontal jump
        elif abs(self._player[0] - x) == 2:
            if self.hor_jump_check(x, y) is False:
                return False

        # checks for fences
        elif self._player[0] - x == 1:
            if '|' in self.vert_fence_conversion(x + 1, y):
                print("fence left")
                return False
        elif self._player[0] - x == -1:
            if '|' in self.vert_fence_conversion(x, y):
                print("fence right")
                return False

    def vert_jump_check(self, x, y):
        """
        Takes x and y, checks if vertical jump is valid,
        returns False to vertical_check if move is invalid
        """
        # down jump
        if self._player[1] - y == 2:
            if 'P' not in self.pawn_conversion(x, y + 1):
                return False
            elif self.hor_fence_conversion(x, y + 2) == '+==':
                return False
            elif self.hor_fence_conversion(x, y + 1) == "+==":
                return False

        # up jump
        else:
            if 'P' not in self.pawn_conversion(x, y - 1):
                return False
            elif self.hor_fence_conversion(x, y - 1) == '+==':
                return False
            elif self.hor_fence_conversion(x, y) == "+==":
                return False

    def hor_jump_check(self, x, y):
        """
        Takes x and y, checks if horizontal jump is valid,
        returns False to vertical_check if move is invalid
        """
        # right jump
        if self._player[0] - x == 2:
            if 'P' not in self.pawn_conversion(x + 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x + 2, y):
                return False
            elif '|' in self.vert_fence_conversion(x + 1, y):
                return False

        # left jump
        else:
            if 'P' not in self.pawn_conversion(x - 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x - 1, y):
                return False
            elif '|' in self.vert_fence_conversion(x, y):
                return False

    def diagonal_check(self, x, y):
        """
        Takes x and y, determines direction of diagonal move,
        calls appropriate method to check validity, returns
        False to move_direction if move is invalid
        """
        # up right
        if self._player[0] - x == -1:
            if self._player[1] - y == 1:
                if self.up_right_check(x, y) is not True:
                    return False

        # down right
        if self._player[0] - x == -1:
            if self._player[1] - y == -1:
                if self.down_right_check(x, y) is not True:
                    return False

        # down left
        if self._player[0] - x == 1:
            if self._player[1] - y == -1:
                if self.down_left_check(x, y) is not True:
                    return False

        # up left
        if self._player[0] - x == 1:
            if self._player[1] - y == 1:
                if self.up_left_check(x, y) is not True:
                    return False

    def up_right_check(self, x, y):    # these checks will return True
        """
        Takes x and y, checks validity of up right move,
        returns False to diagonal_check if move is invalid
        """
        if 'P' in self.pawn_conversion(x - 1, y):
            if self.hor_fence_conversion(x - 1, y) == '+==':
                if self.hor_fence_conversion(x - 1, y + 1) != '+==':
                    if '|' not in self.vert_fence_conversion(x, y):
                        return True
        elif 'P' in self.pawn_conversion(x, y + 1):
            if '|' in self.vert_fence_conversion(x + 1, y + 1):
                if '|' not in self.vert_fence_conversion(x, y + 1):
                    if self.hor_fence_conversion(x, y + 1) != '+==':
                        return True

    def down_right_check(self, x, y):
        """
        Takes x and y, checks validity of down right move,
        returns False to diagonal_check if move is invalid
        """
        if 'P' in self.pawn_conversion(x, y - 1):
            if '|' in self.vert_fence_conversion(x + 1, y - 1):
                if '|' not in self.vert_fence_conversion(x, y - 1):
                    if self.hor_fence_conversion(x, y) != '+==':
                        return True
        elif 'P' in self.pawn_conversion(x - 1, y):
            if self.hor_fence_conversion(x - 1, y + 1) == '+==':
                if self.hor_fence_conversion(x - 1, y) != '+==':
                    if '|' not in self.vert_fence_conversion(x, y):
                        return True

    def down_left_check(self, x, y):
        """
        Takes x and y, checks validity of down left move,
        returns False to diagonal_check if move is invalid
        """
        if 'P' in self.pawn_conversion(x + 1, y):
            if self.hor_fence_conversion(x + 1, y + 1) == '+==':
                if self.hor_fence_conversion(x + 1, y) != '+==':
                    if '|' not in self.vert_fence_conversion(x + 1, y):
                        return True
        elif 'P' in self.pawn_conversion(x, y - 1):
            if '|' in self.vert_fence_conversion(x, y - 1):
                if '|' not in self.vert_fence_conversion(x + 1, y - 1):
                    if self.hor_fence_conversion(x, y) != '+==':
                        return True

    def up_left_check(self, x, y):
        """
        Takes x and y, checks validity of up left move,
        returns False to diagonal_check if move is invalid
        """
        if 'P' in self.pawn_conversion(x, y + 1):
            if '|' in self.vert_fence_conversion(x, y + 1):
                if '|' not in self.vert_fence_conversion(x + 1, y + 1):
                    if self.hor_fence_conversion(x, y + 1) != '+==':
                        return True
        if 'P' in self.pawn_conversion(x + 1, y):
            if self.hor_fence_conversion(x + 1, y) == '+==':
                if self.hor_fence_conversion(x + 1, y + 1) != '+==':
                    if '|' not in self.vert_fence_conversion(x + 1, y):
                        return True

    def place_fence(self, turn, direction, position):
        """
       Takes turn, direction and position, does initial fence
        placement check which calls correct_turn to verify move
        is in turn, calls fences_left to verify player has fences
        remaining, calls fence_check to check if fence placement is
        valid, updates player's fence count if placement is valid,
        and returns False if move is invalid
        """
        x = position[0]
        y = position[1]

        # check if move is in turn
        if self.correct_turn(turn) is False:
            return False

        # check if player has fences left to place
        elif self.remaining_fences(turn) is False:
            return False

        # send to check if fence placement is valid
        elif self.fence_check(direction, position) is False:
            return False

        # check fair play rule if fence placement is valid
        return self.is_fair_play(turn, direction, x, y)

    def remaining_fences(self, turn):
        """
        Takes turn, checks if player has any fences left to place
        """
        if turn == 1:
            if self._p1Fences == 0:
                return False
        else:
            if self._p2Fences == 0:
                return False

    def fence_check(self, direction, position):
        """
        Takes direction and position, checks if a fence already exists
        in position and returns False if it does, places fence if not
        """
        x = position[0]
        y = position[1]

        # horizontal fence check
        if direction == 'h':
            if self.hor_fence_conversion(x, y) == '+==':
                return False
            else:
                xf = y * 2
                yf = x
                self._board[xf][yf] = '+=='

        # vertical fence check
        elif direction == 'v':
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

    def remove_fence(self, direction, x, y):
        """
        Takes direction, x, and y, removes fence
        from that position of board. Called after
        fair play rule has been broken
        """
        # remove horizontal fence
        if direction == "h":
            xf = y * 2
            yf = x
            self._board[xf][yf] = '+  '

        # remove vertical fence
        elif direction == 'v':
            xf = y * 2 + 1
            yf = x
            if 'P1' in self._board[xf][yf]:
                self._board[xf][yf] = ' P1'
            elif 'P2' in self._board[xf][yf]:
                self._board[xf][yf] = ' P2'
            else:
                self._board[xf][yf] = '   '

    def is_fair_play(self, turn, direction, x, y):
        """Takes turn, direction, x, and y, called after otherwise
        valid fence has been placed to determine if the placement
        breaks the fair play rule by bocking off all paths to the
        opponent's baseline. If fair play rule has been broken, calls
        remove_fence to remove the fence from the board and returns
        'breaks the fair play rule'. If fair play rule has not been
        broken, decrements player's fence inventory and sets turn for
        next player"""
        import copy
        self._fair_play_board1 = copy.deepcopy(self._fair_play_board)
        if turn == 1:
            x1 = self._p2[0]
            y1 = self._p2[1]
            if self.rec_fair_play(1, x1, y1) is not True:
                self.remove_fence(direction, x, y)
                return 'breaks the fair play rule'
            else:
                self._p1Fences -= 1
                self._turn = 2
                return True
        elif turn == 2:
            x2 = self._p1[0]
            y2 = self._p1[1]
            if self.rec_fair_play(2, x2, y2) is not True:
                self.remove_fence(direction, x, y)
                return 'breaks the fair play rule'
            else:
                self._p2Fences -= 1
                self._turn = 1
                return True

    def rec_fair_play(self, turn, x, y):
        """
        Takes turn, x, and y, determines if player has at least one path
        to the opponent's baseline. Checks for fences and recursively calls all four move
        directions which are not obstructed by fences, flipping tiles from False to True.
        Returns True if a tile on the opponent's row has been flipped
        """
        self._fair_play_board1[y][x] = True
        paintUp = False
        paintRight = False
        paintDown = False
        paintLeft = False
        # player 1 placed fence, checks if player 2 has access to player 1's baseline
        if turn == 1:
            if True in self._fair_play_board1[0]:
                return True
        # player 2 placed fence, checks if player 1 has access to player 2's baseline
        elif turn == 2:
            if True in self._fair_play_board1[8]:
                return True

        if self.hor_fence_conversion(x, y) != '+==':
            if self._fair_play_board1[y - 1][x] is False:
                paintUp = self.rec_fair_play(turn, x, y - 1)

        if self.hor_fence_conversion(x, y + 1) != '+==':
            if self._fair_play_board1[y + 1][x] is False:
                paintDown = self.rec_fair_play(turn, x, y + 1)

        if '|' not in self.vert_fence_conversion(x + 1, y):
            if self._fair_play_board1[y][x + 1] is False:
                paintRight = self.rec_fair_play(turn, x + 1, y)

        if '|' not in self.vert_fence_conversion(x, y):
            if self._fair_play_board1[y][x - 1] is False:
                paintLeft = self.rec_fair_play(turn, x - 1, y)

        if paintUp or paintRight or paintDown or paintLeft is True:
            return True

    def check_for_win(self, turn, y):
        """
        Takes turn and y, updates winner data member if game has been won
        Called by move_pawn after move is determined to be valid
        """
        if turn == 1:
            if y == 8:
                self._winner = 1
        else:
            if y == 0:
                self._winner = 2

    def is_winner(self, player):
        """
        Takes player, returns True if player has won, False otherwise
        """
        if self._winner == player:
            return True
        else:
            return False


def main():
    # game with not many fences, p2 wins
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
    print(q.move_pawn(2, (3, 3)))
    print(q.move_pawn(1, (3, 5)))
    print(q.move_pawn(2, (3, 2)))
    print(q.move_pawn(1, (3, 6)))
    print(q.move_pawn(2, (3, 1)))
    print(q.place_fence(1, 'h', (3, 1)))
    print(q.move_pawn(2, (4, 1)))
    print(q.move_pawn(1, (3, 7)))
    print(q.move_pawn(2, (4, 0)))
    print(q.is_winner(2))
    print(q.move_pawn(1, (3, 8)))
    q.print_board()


if __name__ == '__main__':
    main()


