from cdkk.cdkkUtils import *

# --------------------------------------------------


class cdkkApp:
    _cdkkApp = None
    default_config = {
        "auto_start": True       # Automatically start game
    }

    def __init__(self, app_config=None):
        # 0=Pre-init, 1=Initialised, 2=Game-in-progess, 3=Game over, 8=Fail-and-exit, 9=Quitting
        self._game_status = 0
        self._config = {}
        self.update_config(merge_dicts(cdkkApp.default_config, app_config))
        cdkkApp._cdkkApp = self

    @property
    def game_in_progress(self):
        return (self._game_status == 2)

    def get_config(self, attribute, default=None):
        return self._config.get(attribute, default)

    def set_config(self, attribute, new_value):
        if attribute is not None:
            self._config[attribute] = new_value
            if attribute == "slow_update_time":
                self._slow_update_timer = Timer(new_value/1000.0)

    def update_config(self, *updated__configs):
        for cfg in updated__configs:
            if cfg is not None:
                for key, value in cfg.items():
                    self.set_config(key, value)

    def init(self):
        self._game_status = 1
        return True

    def start_game(self):
        self._game_status = 2

    def end_game(self):
        self._game_status = 3

    def exit_app(self):
        self._game_status = 9

    def manage_events(self):
        pass

    def update(self):
        pass

    def draw(self, flip=True):
        pass

    def manage_loop(self):
        pass

    def cleanup(self):
        pass

    def execute(self):
        if self.init() == False:
            self._game_status = 8

        if self.get_config("auto_start"):
            self.start_game()

        while self._game_status < 8:
            self.manage_events()
            self.update()
            self.draw()
            self.manage_loop()

        self.cleanup()

# --------------------------------------------------
