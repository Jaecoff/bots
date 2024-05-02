from src.games.game import Game
import random
from copy import deepcopy
from threading import Thread


class Bot():
    def __init__(self,
                 _game: Game = None):
        self.game = _game
        self.states = {}
    def __str__(self):
        return f"{self.game}"
    def __states_to_string__(self):
        for key, value in self.states.items():
            state = self.game.key_to_state(key)
            board = self.game.state_to_string(state)
            print(board, value, key, "\n")

    # ------------------------
    # Best move methods:
    # ------------------------
    def best_move_01(self,
                     _state: dict = None,
                     _player: int = None) -> int:
        _state = self.game.copy_state(_state)
        if _player is  None: _player = self.game.next()
        moves = self.game.moves(_state)
        for move in moves:
            new_state = self.game.move(move,
                                       _state)
            if self.game.winner(new_state) == _player: return move
        assert len(moves) > 0, "error!1! No mvoes :("
        return random.choice(moves)

    # -> first winning move, where the enemy hasn't had a chance to win (or random move) <-
    # BrethFirstSearch
    def best_move_08_bfs(self,
                         _state=None,
                         player=None,
                         depth=3):
        if depth == 0: return random.choice(self.game.moves(_state = _state))
        state = self.game.copy_state(_state = _state)
        if player is None: player = self.game.next()
        key = self.game.state_to_key(_state = state)
        if key not in self.states.keys(): self.states[key] = self.game.moves(_state = state)
        moves = deepcopy(self.states[key])
        for move in moves:
            new_state = self.game.move(move = move,
                                       _state = state)
            winner = self.game.winner(_state = new_state)
            if winner == player:
                self.states[key] = [move]
                break
            if winner != 0:
                self.states[key].remove(move)
                continue
            moves_02 = []
            for move_02 in self.game.moves(_state = new_state):
                state_02 = self.game.move(move = move_02,
                                          _state = new_state)
                winner_02 = self.game.winner(_state = state_02)
                if winner_02 not in (player, 0):
                    self.states[key].remove(move)
                    moves_02 = []
                    break
                moves_02 += [(move_02, state_02)]
            for move_02 in moves_02:
                next_move = self.best_move_08_bfs(_state = state_02,
                                                  player = player,
                                                  depth = depth-1)
                if next_move is None:
                    self.states[key].remove(move)
                    break
        if len(self.states[key]) == 0:
            if _state is None:
                if len(moves) == 0: return random.choice(self.game.moves(_state = state))
                return random.choice(moves)
            return None
        return random.choice(self.states[key])

    # DepthFirstSearch
    def best_move_08_dfs(self,
                         _state=None,
                         player=None,
                         depth=3):
        if depth == 0: return random.choice(self.game.moves(_state = _state))
        state = self.game.copy_state(_state = _state)
        if player is None: player = self.game.next()
        key = self.game.state_to_key(_state = state)
        if key not in self.states.keys(): self.states[key] = self.game.moves(_state = state)
        moves = deepcopy(self.states[key])
        for move in moves:
            new_state = self.game.move(move = move,
                                       _state = state)
            winner = self.game.winner(_state = new_state)
            if winner == player:
                self.states[key] = [move]
                break
            if winner != 0:
                self.states[key].remove(move)
                continue
            for move_02 in self.game.moves(_state = new_state):
                state_02 = self.game.move(move = move_02,
                                          _state = new_state)
                winner_02 = self.game.winner(_state = state_02)
                if winner_02 not in (player, 0):
                    self.states[key].remove(move)
                    break
                next_move = self.best_move_08_dfs(_state = state_02,
                                                  player = player,
                                                  depth = depth-1)
                if next_move is None:
                    self.states[key].remove(move)
                    break
        if len(self.states[key]) == 0:
            if _state is None:
                if len(moves) == 0: return random.choice(self.game.moves(_state = state))
                return random.choice(moves)
            return None
        return random.choice(self.states[key])


    # def best_09(self, _state=None, _player=None, depth=3):
    #     if depth == 0: return random.choice(self.game.moves(_state = _state))
    #     state = self.game.copy_state(_state  = _state)
    #     if _player is None: player = self.game.next()
    #     key = self.game.state_to_key(_state = state)
    #     if key not in 



    # def best_move_09_threading(self,
    #                            _state=None,
    #                            player=None,
    #                            depth=3):
    #     if depth == 0: return random.choice(self.game.moves(_state = _state))
    #     state = self.game.copy_state(_state = _state)
    #     if player is None: player = self.game.next()
    #     key = self.game.state_to_key(_state = state)
    #     if key not in self.states.keys(): self.states[key] = self.game.moves(_state = state)
    #     moves = deepcopy(self.states[key])
    #     for move in moves:
    #         new_state = self.game.move(move = move,
    #                                    _state = state)
    #         winner = self.game.winner(_state = new_state)
    #         if winner == player:
    #             self.states[key] = [move]
    #             break
    #         if winner != 0:
    #             self.states[key].remove(move)
    #             continue
    #         moves_02 = []
    #         for move_02 in self.game.moves(_state = new_state):
    #             state_02 = self.game.move(move = move_02,
    #                                       _state = new_state)
    #             winner_02 = self.game.winner(_state = state_02)
    #             if winner_02 not in (player, 0):
    #                 self.states[key].remove(move)
    #                 moves_02 = []
    #                 break
    #             moves_02 += [(move_02, state_02)]
    #         for move_02 in moves_02:
    #             next_move = self.best_move_08_bfs(_state = state_02,
    #                                               player = player,
    #                                               depth = depth-1)
    #             if next_move is None:
    #                 self.states[key].remove(move)
    #                 break
    #     if len(self.states[key]) == 0:
    #         if _state is None:
    #             if len(moves) == 0: return random.choice(self.game.moves(_state = state))
    #             return random.choice(moves)
    #         return None
    #     return random.choice(self.states[key])

