from sys import maxsize
from cdkkConfig import Config

class Game:
    # Methods to update in sub-classes: init, start, check, update
    default_config = {}

    def __init__(self, init_config={}):
        self.config = Config(Game.default_config)
        self.config.update(init_config)
        self._game_count = self._turn_count = self._current_player = self._num_players = 0
        self._player_wins = self._scores = []
        self.options: list[str] = []
        self.next_after_update = True
        self.status = -2
            # Game status:
            #   -2 = No game in progress
            #   -1 = Game in progress
            #    0 = Game over - Draw
            # 1-98 = Game over - Win - Number of winning player
            #   99 = Game over - Loss
            # 100+ = Game over - Error number

    @property
    def game_over(self) -> bool:
        # Return True if the game is over
        return (self.status >= 0)

    @property
    def max_turns(self) -> int:
        return int(self.config.get("max_turns", maxsize))

    @property
    def current_player(self) -> int:
        return self._current_player

    @property
    def players(self) -> int:
        return self._num_players

    @players.setter
    def players(self, value: int):
        self._num_players = value

    @property
    def scores(self) -> list[int]:
        return self._scores

    @property
    def counts(self) -> dict:
        return {
            "players":self._num_players
            ,"turns":self._turn_count
            ,"max_turns":self.max_turns
            ,"games":self._game_count
            ,"scores":self._scores
            ,"wins":self._player_wins
            }

    def set_score(self, player:int, score:int) -> int:
        if player < 0 or player >= self._num_players:
            return -1
        self._scores[player] = score
        return score

    def init(self) -> bool:
        # Return True if initialised OK
        if self._num_players == 0:
            self._num_players = int(self.config.get("players", 1))
        self._scores = [0 for x in range(self.players)]
        self._player_wins = [0 for x in range(self.players)]
        return True

    def start(self):
        self._game_count += 1
        self._turn_count = 1
        self._current_player = 1
        self.status = -1

    def calc_options(self) -> list[str]:
        # Calculate possible turns
        self.options.clear()
        return self.options

    def check(self, turn) -> str:
        # Return "" if this turn is valid. Otherwise an error message.
        if len(self.options) > 0 and turn not in self.options:
            return "That is not a valid option."
        return ("")

    def take(self, turn):
        # Run game logic, update game elements
        pass

    def calc_scores(self) -> None:
        # Calculate each players score
        pass

    def update_status(self, turn) -> int:
        return self.status

    def update(self, turn):
        # Take turn for player: update game elements and run game logic
        self.take(turn)
        self.calc_scores()
        self.update_status(turn)
        if not self.game_over:
            self._turn_count += 1
            if self.next_after_update:
                self._current_player += 1
                if self._current_player > self._num_players:
                    self._current_player = 1
        else:
            if (self.status > 0 and self.status < 99):
                self._player_wins[self.status - 1] += 1

# ----------------------------------------

if __name__ == '__main__':
    game = Game()
    x = game.counts
    print("Done")
