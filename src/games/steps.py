from src.games.game import Game
from math import log2


class Steps(Game):
    # class functions
    def __init__(self,
                 _length: int = 12,
                 _pos1: int = 1,
                 _pos2: int = 12,
                 _next: int = 1) -> None:
        self.length = _length
        self.position_1 = _pos1
        self.position_2 = _pos2
        self.state = {"pos1" : self.position_1,
                      "pos2" : self.position_2,
                      "next" : _next
                     }
    def __str__(self):
        return self.state_to_string(self.state)

    # state functions
    def next(self):
        return self.state["next"]
    def state_to_string(self, _state: dict) -> str:
        builder = ["|"]
        builder += [" "]*self.length
        builder += ["|"]
        builder[_state["pos1"]] = "X"
        builder[_state["pos2"]] = "O"
        return "".join(builder)
    def copy_state(self, _state: dict = None) -> dict:
        if _state is None: output_state = self.state.copy()
        else: output_state = _state.copy()
        return output_state
    def state_to_key(self, _state: dict = None) -> int:
        state = self.copy_state(_state)
        key = state["next"] - 1
        key |= state["pos1"] << 1
        key |= state["pos2"] << (int(log2(self.length)) + 1)
        return key
    def key_to_state(self, _key: int) -> dict:
        state = {}
        state["next"] = (_key & 1) + 1
        state["pos1"] = 0b1111 & (_key >> 1)
        state["pos2"] = 0b1111 & (_key >> (log2(self.length) + 1))
        return state

    # game functions
    def winner(self, _state: dict = None) -> int:
        state = self.copy_state(_state)
        distance = state["pos2"] - state["pos1"]
        if distance > 1: return 0 # not done yet
        if distance == 1:
            if state["next"] == 1: return 2 # player 2 wins
            else: return 1 # player 1 wins
        else: return -1 # tie

    def moves(self, _state: dict = None) -> list:
        state = self.copy_state(_state)
        if state["pos2"] - state["pos1"] > 2: return [1,2]
        if state["pos2"] - state["pos1"] > 1: return [1]
        return []

    def move(self, move: int, _state: dict = None):
        state =  self.copy_state(_state)
        if state["next"] == 1:
            state["pos1"] += move
            state["next"] = 2
        else:
            state["pos2"] -= move
            state["next"] = 1
        if _state is None: self.state = self.copy_state(state)
        return state

