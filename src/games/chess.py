from src.games.game import Game
"""
pieces:
    dec bin     chr name
    1   0001    wp  white pawn
    2   0010    wb  white bishop
    3   0011    wk  white knight
    4   0100    wr  white rook (tower)
    5   0101    wq  white queen
    6   0110    wK  white king
    8   1000    bp  black pawn
    9   1001    bb  black bishop
    10  1010    bk  black knight
    11  1011    br  black rook (tower)
    12  1100    bq  black queen
    13  1101    bK  black king
"""
piece_symbols = {
    0:"  ",
    1:"[p", 2:"[b", 3:"[k", 4:"[r", 5:"[q", 6:"[K",
    8:" p", 9:" b", 10:" k", 11:" r", 12:" q", 13:" K"}

start_setup = [
    [11,10,9,12,13,9,10,11],
    [8,8,8,8,8,8,8,8],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [4,3,2,5,6,2,3,4]]

class Chess(Game):
    def __init__(self, setup=start_setup, next: int = 1) -> None:
        self.length = len(setup)
        self.width = len(setup[0])
        self.state = {"map": [0 for _ in range(self.length)],
                      "next": next}
        self.state = self.setup_map(setup)
    def __str__(self) -> str:
        return self.state_to_string(self.state)

    def next(self):
        return self.state["next"]
    def state_to_string(self, state):
        output = " " + "__"*self.width
        for row in range (self.length):
            output += "\n|"
            for column in range(self.width):
                value = self.get_cell(row, column, state)
                output += piece_symbols[value]
            output += "|"
        output += "\n " + u"\u203e\u203e"*self.width # UTF-8 chart 203E is "upperline"
        return output
    def state_to_key(self, _state=None):
        state = self.copy_state(_state)
        key = ""
        for row in state["map"]:
            key += str(row) + ","
        key += str(state["next"])
        return key
    def key_to_state(self, key):
        board = []
        for value in key.split(",")[:-1]:
            board += [int(value)]
        next = int(key[-1])
        return (board, next)
    def get_next_player(self, _state=None):
        state = self.copy_state(_state)
        player = state["next"]
        if player == 1: player = 2
        elif player == 2: player = 1
        return player
    def setup_map(self, setup):
        state = {"map": [0 for _ in range(self.length)], "next": self.state["next"]}
        for row, row_content in enumerate(setup):
            for column, value in enumerate(row_content):
                self.set_cell(row, column, value, state, True)
        return state
    def set_cell(self, row, column, value, _state=None, set_cell=False):
        if set_cell: state = _state
        else: state = self.copy_state(_state)
        state["map"][row] &= ~(0b1111 << (column * 4))
        state["map"][row] |= (value << (column * 4))
        return state
    def get_cell(self, row, column, state):
        value = state["map"][row] >> (column*4) & 0b1111
        return value
    def player_from_position(self, row, column, _state=None):
        value = self.get_cell(row, column, _state)
        if 1 <= value <= 6: player = 1
        elif 8 <= value <= 13: player = 2
        else: player = 0
        return player
    def player_from_value(self, value):
        if 1 <= value <= 6: player = 1
        elif 8 <= value <= 13: player = 2
        else: player = 0
        return player
    def player_from_colour(self, colour):
        if colour == "nothing": player = 0
        elif colour == "white": player = 1
        elif colour == "black": player = 2
        return player
    def get_player(self, row=None, column=None, _state=None, _value=None, colour=None):
        if row is not None and column is not None and _state is not None: value = self.get_cell(row, column, _state)
        elif _value is not None: value = _value
        elif colour is not None:
            if colour == "nothing": return 0
            elif colour == "white": return 1
            elif colour == "black": return 2
        if 1 <= value <= 6: player = 1
        elif 8 <= value <= 13: player = 2
        else: player = 0
        return player
    def get_colour(self, row=None, column=None, _state=None, _value=None):
        if _value is None:
            state = self.copy_state(_state)
            value = self.get_cell(row, column, state)
        elif row is None and column is None and _state is None: value = _value
        else: raise Exception("Either row, column, _state must be None or _value must be None")
        if 1 <= value <= 6: colour = "white" # 1
        elif 8 <= value <= 13: colour = "black" # 2
        else: colour = "nothing" # 0
        return colour
    def find_value(self, piece_value, _state=None):
        state = self.copy_state(_state)
        for row in range(self.length):
            for column in range(self.width):
                value = self.get_cell(row=row, column=column, state=state)
                if value == piece_value: return True
        return False
    def copy_state(self, _state=None):
        if _state is None: state = {"map": self.state["map"].copy(), "next": self.state["next"]}
        else: state = {"map": _state["map"].copy(), "next": _state["next"]}
        return state

    def moves(self, _state=None):
        state = self.copy_state(_state)
        moves = []
        for row in range(self.width):
            for column in range(self.length):
                value = self.get_cell(row, column, state)
                player = self.player_from_value(value)
                if value == 0 or player != state["next"]: continue
                elif value in [1,8]: moves += self.moves_pawn(row, column, state)
                elif value in [2,9]: moves += self.moves_bishop(row, column, state)
                elif value in [3,10]: moves += self.moves_knight(row, column, state)
                elif value in [4,11]: moves += self.moves_rook(row, column, state)
                elif value in [5,12]: moves += self.moves_queen(row, column, state)
                elif value in [6,13]: moves += self.moves_king(row, column, state)
                else: raise IndexError(f"Unknown value {value} at position ({row},{column})")
        return moves

    def moves_pawn(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        if player == 1: row_move = -1 # white
        elif player == 2: row_move = 1 # black
        for (target_row, target_column) in [(row+row_move, column),
                                            (row+row_move*2, column),
                                            (row+row_move, column-1),
                                            (row+row_move, column+1)]:
            if target_row < 0 or self.length <= target_row: continue # leaving the board
            if target_column < 0 or self.width <= target_column: continue # leaving the board
            target_player = self.get_player(row=target_row, column=target_column, _state=state)
            if target_player == player: continue # friendly fire
            if target_column == column and target_player != 0: continue # attacking straight
            if target_column != column and target_player == 0: continue # moving diagonally
            if row not in (1,6) and abs(target_row-row) == 2: continue # double steps
            moves += [(row, column, target_row, target_column)]
        return moves
    def moves_bishop(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        directions = {"NW": True, "NE": True, "SW": True, "SE": True}
        for i in range(1, max(self.width,self.length)):
            for (target_row, target_column, direction) in [(row-i, column-i, "NW"),
                                                           (row-i, column+i, "NE"),
                                                           (row+i, column-i, "SW"),
                                                           (row+i, column+i, "SE")]:
                if not directions[direction]: continue # passing another piece
                if target_row < 0: # leaving the board north
                    directions["NW"] = False
                    directions["NE"] = False
                    continue
                if self.length <= target_row: # leaving the board south
                    directions["SW"] = False
                    directions["SE"] = False
                    continue
                if target_column < 0: # leaving the board west
                    directions["NW"] = False
                    directions["SW"] = False
                    continue
                if self.width <= target_column: # leaving the board east
                    directions["NE"] = False
                    directions["SE"] = False
                    continue
                target_player = self.get_player(row=target_row, column=target_column, _state=state)
                if target_player != 0: directions[direction] = False # targeting another piece
                if target_player == player: continue # friendly fire
                moves += [(row, column, target_row, target_column)]
            if all(not direction for direction in directions): break
        return moves
    def moves_knight(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        for (target_row, target_column) in [(row+1, column+2),
                                            (row+1, column-2),
                                            (row+2, column+1),
                                            (row+2, column-1),
                                            (row-1, column+2),
                                            (row-1, column-2),
                                            (row-2, column+1),
                                            (row-2, column-1)]:
            if target_row < 0 or self.length <= target_row: continue # leaving the board
            if target_column < 0 or self.width <= target_column: continue # leaving the board
            target_player = self.get_player(row=target_row, column=target_column, _state=state)
            if target_player == player: continue # friendly fire
            moves += [(row, column, target_row, target_column)]
        return moves
    def moves_rook(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        directions = {"N": True, "E": True, "S": True, "W": True}
        for i in range(1, max(self.width,self.length)):
            for (target_row, target_column, direction) in [(row-i, column, "N"),
                                                           (row, column+i, "E"),
                                                           (row+i, column, "S"),
                                                           (row, column-i, "W")]:
                if not directions[direction]: continue # passing another piece
                if target_row < 0: # leaving the board north
                    directions["N"] = False
                    continue
                if self.length <= target_row: # leaving the board south
                    directions["S"] = False
                    continue
                if target_column < 0: # leaving the board west
                    directions["W"] = False
                    continue
                if self.width <= target_column: # leaving the board east
                    directions["E"] = False
                    continue
                target_player = self.get_player(row=target_row, column=target_column, _state=state)
                if target_player != 0: directions[direction] = False # targeting another piece
                if target_player == player: continue # friendly fire
                moves += [(row, column, target_row, target_column)]
            if all(not direction for direction in directions): break
        return moves
    def moves_queen(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        directions = {"N": True, "E": True, "S": True, "W": True, "NW": True, "NE": True, "SW": True, "SE": True}
        for i in range(1, max(self.width,self.length)):
            for (target_row, target_column, direction) in [(row-i, column, "N"),
                                                           (row, column+i, "E"),
                                                           (row+i, column, "S"),
                                                           (row, column-i, "W"),
                                                           (row-i, column-i, "NW"),
                                                           (row-i, column+i, "NE"),
                                                           (row+i, column-i, "SW"),
                                                           (row+i, column+i, "SE")]:
                if not directions[direction]: continue # passing another piece
                if target_row < 0: # leaving the board north
                    directions["N"] = False
                    directions["NW"] = False
                    directions["NE"] = False
                    continue
                if self.length <= target_row: # leaving the board south
                    directions["S"] = False
                    directions["SW"] = False
                    directions["SE"] = False
                    continue
                if target_column < 0: # leaving the board west
                    directions["W"] = False
                    directions["NW"] = False
                    directions["SW"] = False
                    continue
                if self.width <= target_column: # leaving the board east
                    directions["E"] = False
                    directions["NE"] = False
                    directions["SE"] = False
                    continue
                target_player = self.get_player(row=target_row, column=target_column, _state=state)
                if target_player != 0: directions[direction] = False # targeting another piece
                if target_player == player: continue # friendly fire
                moves += [(row, column, target_row, target_column)]
            if all(not direction for direction in directions): break
        return moves
    def moves_king(self, row, column, state):
        moves = []
        player = self.get_player(row=row, column=column, _state=state)
        for (target_row, target_column) in [(row-1, column),
                                            (row, column+1),
                                            (row+1, column),
                                            (row, column-1),
                                            (row-1, column-1),
                                            (row-1, column+1),
                                            (row+1, column-1),
                                            (row+1, column+1)]:
            if target_row < 0 or self.length <= target_row: continue # leaving the board
            if target_column < 0 or self.width <= target_column: continue # leaving the board
            target_player = self.get_player(row=target_row, column=target_column, _state=state)
            if target_player == player: continue # friendly fire
            moves += [(row, column, target_row, target_column)]
        return moves

    def move(self, move, _state=None):
        state = self.copy_state(_state)
        (row, column, target_row, target_column) = move
        value = self.get_cell(row, column, state)
        self.set_cell(target_row, target_column, value, state, True) # target cell = value
        self.set_cell(row, column, 0, state, True) # source cell = 0
        state["next"] = self.get_next_player(state)
        if _state is None: self.state = state
        return state

    def winner(self, _state=None):
        state = self.copy_state(_state)
        black_king_found = self.find_value(6, state)
        white_king_found = self.find_value(13, state)
        if not black_king_found and not white_king_found: winner = -1 # tie...
        elif not black_king_found: winner = 1 # player 1 (white)
        elif not white_king_found: winner = 2 # player 2 (black)
        else: winner = 0 # not done
        return winner

