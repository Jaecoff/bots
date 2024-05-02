from src.games.game import Game


class TicTacToe(Game):
    # class functions
    def __init__(self,
                 _width: int = 3,
                 _length: int = 3,
                 _next: int = 1) -> None:
        self.width = _width
        self.length = _length
        self.state = {"map": [[0 for _ in range(_length)] for _ in range(_width)],
                      "next": _next
                     }
    def __str__(self):
        return self.state_to_string(self.state)

    # state functions
    def next(self):
        return self.state["next"]
    def state_to_string(self, _state: dict) -> str:
        state = self.copy_state(_state)
        builder = "|"
        for row in state["map"]:
            for value in row:
                if value == 1: builder += "><"
                elif value == 0: builder += "  "
                elif value == 2: builder += "()"
            builder += "|\n|"
        return builder[:-1]
    def copy_state(self, _state: dict = None) -> dict:
        if _state is None:
            output_map = [row.copy() for row in self.state["map"]]
            output_next = self.state["next"]
        else:
            output_map = [row.copy() for row in _state["map"]]
            output_next = _state["next"]
        return {"map": output_map, "next": output_next}
    def state_to_key(self, _state: dict = None) -> int:
        state = self.copy_state(_state)
        key = state["next"] - 1
        position = 1
        for row in state["map"]:
            for value in row:
                key |= (value << position)
                position += 2
        return key
    def key_to_state(self, _key: int) -> dict:
        next = (_key & 1) + 1
        position = 1
        map = [[0 for _ in range(self.width)] for _ in range(self.length)]
        for row in range(self.width):
            for column in range(self.length):
                value = (_key >> position) & 0b11
                map[row][column] = value
                position += 2
        return {"next": next, "map": map}

    # game functions
    def winner(self, _state: dict = None) -> int:
        state = self.copy_state(_state)
        for (r1, c1, r2, c2, r3, c3) in [(0,0,0,1,0,2),
                                         (1,0,1,1,1,2),
                                         (2,0,2,1,2,2),
                                         (0,0,1,0,2,0),
                                         (0,1,1,1,2,1),
                                         (0,2,1,2,2,2),
                                         (0,0,1,1,2,2),
                                         (0,2,1,1,2,0)]:
            if state["map"][r1][c1] == state["map"][r2][c2] == state["map"][r3][c3] == 1: return 1
            if state["map"][r1][c1] == state["map"][r2][c2] == state["map"][r3][c3] == 2: return 2
        count = sum(sum(1 for value in row if value != 0) for row in state["map"])
        if count == 9: return -1
        return 0

    def moves(self, _state: dict = None) -> list:
        state = self.copy_state(_state)
        moves = []
        for row in range(self.width):
            for column in range(self.length):
                if state["map"][row][column] == 0: moves += [(row, column)]
        if len(moves) == 0:
            pass
        return moves

    def move(self, move: int, _state: dict = None):
        state =  self.copy_state(_state)
        (row, column) = move
        state["map"][row][column] = state["next"]
        if state["next"] == 1: state["next"] = 2
        else: state["next"] = 1
        if _state is None: self.state = self.copy_state(state)
        return state
