# from src.games.game import Game
from src.games.steps import Steps
from src.games.connect_four import ConnectFour
from src.games.chess import Chess
from src.games.tictactoe import TicTacToe
from src.bot.bot import Bot


# bot = Bot(Steps())
# bot = Bot(TicTacToe())
bot = Bot(ConnectFour())
# bot = Bot(Chess())

# bot = Bot()

for game_count in range(50):
    # bot.game.setup_map()
    # bot.game = Steps()
    # bot.game = TicTacToe()
    bot.game = ConnectFour()
    # bot.game = Chess()

    for i in range(100):
        if bot.game.next() == 1:
            move = bot.best_move_08_bfs(depth = 4)
        else: move = bot.best_move_08_bfs(depth = 1)
        bot.game.move(move)
        winner = bot.game.winner()
        print(f"\n{bot.game}\n {game_count},{i}:, next: {bot.game.next()}, winner: {winner}, len(states): {len(bot.states)}")
        if winner != 0:
            # if winner in (2, -1):
            #     print("winner:", winner)
            #     assert False, "player 2 won or it's a tie"
            print(f"game: {game_count} winner: {winner}")
            break
