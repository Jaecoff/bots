class Game():
    def next(self, _state: dict = None) -> int: ...
    def state_to_string(self, _state:dict) -> str: ...
    def state_to_key(self, _state: dict) -> int: ...
    def key_to_state(self, key: int) -> dict: ...
    def copy_state(self, _state: dict = None) -> dict: ...

    def move(self, move, _state: dict = None) -> dict: ...
    def moves(self, _state: dict = None) -> list: ...
    def winner(self, _state: dict = None) -> int: ...
