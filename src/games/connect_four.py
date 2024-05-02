from src.games.game import Game



start_setup = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]]

class ConnectFour(Game):
    # class functions
    def __init__(self,
                 _height: int = 6,
                 _width: int = 7,
                 setup = start_setup,
                 _next: int = 1) -> None:
        self.height = _height
        self.width = _width
        self.map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.state = {"map" : self.map,
                      "next" : _next}
        self.state = self.setup_map(setup)
    def __str__(self) -> str:
        return self.state_to_string(self.state)

    # state functions
    def next(self):
        return self.state["next"]
    def setup_map(self, setup):
        state = {"map": [[0 for _ in range(self.width)] for _ in range(self.height)], "next": self.state["next"]}
        return state
    def state_to_string(self, _state: dict) -> str:
        builder = ""
        for row in _state["map"]:
            builder += "\n|"
            for value in row:
                if value == 1: builder += "X"
                elif value == 2: builder += "O"
                else: builder += " "
            builder += "|"
        return builder
    def copy_state(self, _state: dict = None) -> dict:
        """Get a copy of _state or self.state"""
        if _state is None:
            state = self.state.copy()
            state["map"] = self.state["map"].copy()
        else:
            state = _state.copy()
            state["map"] = _state["map"].copy()
        return state
    def key_to_state(self, _key:int) -> dict:
        state = {}
        state["next"] = _key & 0b1 + 1
        state["map"] = [[0 for _ in range(self.width)] for _ in range(self.height)]
        position = 1
        for row in range(self.height):
            for column in range(self.width):
                state["map"][row][column] = (_key >> position) & 0b11
                position += 2
        return self.copy_state(state)
    def state_to_key(self, _state: dict = None) -> int:
        state = self.copy_state(_state)
        key = state["next"] - 1
        position = 1
        for row in state["map"]:
            for value in row:
                key |= (value << position)
                position += 2
        return key

    def winner(self, _state=None):
        state = self.copy_state(_state)
        for row in range(self.height):
            for column in range(self.width):
                if column+3 < self.width:
                    if state["map"][row][column:column+4] == [1,1,1,1]: return 1
                    if state["map"][row][column:column+4] == [2,2,2,2]: return 2
                if row+4 <= self.height:
                    if state["map"][row][column] == state["map"][row+1][column] == \
                       state["map"][row+2][column] == state["map"][row+3][column] == 1: return 1
                    if state["map"][row][column] == state["map"][row+1][column] == \
                       state["map"][row+2][column] == state["map"][row+3][column] == 2: return 2
                if column+3 < self.width and row+4 <= self.height:
                    if state["map"][row][column] == state["map"][row+1][column+1] == \
                       state["map"][row+2][column+2] == state["map"][row+3][column+3] == 1: return 1
                    if state["map"][row][column] == state["map"][row+1][column+1] == \
                       state["map"][row+2][column+2] == state["map"][row+3][column+3] == 2: return 2
                    if state["map"][row][column+3] == state["map"][row+1][column+2] == \
                       state["map"][row+2][column+1] == state["map"][row+3][column] == 1: return 1
                    if state["map"][row][column+3] == state["map"][row+1][column+2] == \
                       state["map"][row+2][column+1] == state["map"][row+3][column] == 2: return 2
        count = sum(sum(1 for value in row if value!=0) for row in state["map"])
        if count == self.height*self.width: return -1
        return 0

    def moves(self, _state: dict = None) -> list:
        """List of possible moves.

        Args:
            _state (dict, optional): Relevant game state. Defaults to None -> current game state.

        Returns:
            list: List of possible moves.
        """
        state = self.copy_state(_state)
        moves = []
        for col in range(self.width):
            if state["map"][0][col] == 0: moves += [col+1]
        return moves

    def move(self, move: int, _state: dict = None) -> dict:
        """Applies _move to _state.

        Args:
            _move (int): Move to perform.
            _state (dict, optional): Relevant game state. Defaults to None -> current game state.

        Returns:
            dict: New state after performing move.
        """
        state = self.copy_state(_state)
        if state["next"] == 1:
            for row in range(self.height-1,-1,-1):
                if state["map"][row][move-1] == 0:
                    state["map"][row] = state["map"][row][:move-1] + \
                                            [1] + \
                                            state["map"][row][move:]
                    state["next"] = 2
                    break
        else:
            for row in range(self.height-1,-1,-1):
                if state["map"][row][move-1] == 0:
                    state["map"][row] = state["map"][row][:move-1] + \
                                            [2] + \
                                            state["map"][row][move:]
                    state["next"] = 1
                    break
        if _state is None:
            self.state = self.copy_state(state)
            self.map = state["map"].copy()
            self.state["next"] = state["next"]
        return state
