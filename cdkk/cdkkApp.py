from cdkk.cdkkUtils import *

# --------------------------------------------------


class cdkkApp:
    _cdkkApp = None
    default_config = {
        "auto_start": True,             # Automatically start game
        "exit_at_end": False,           # Exit the app when game ends
        "read_key_and_process": None    # Default behaviour in manage_events()
    }

    def __init__(self, app_config=None):
        # 0=Pre-init, 1=Initialised, 2=Game-in-progess, 3=Game over, 8=Fail-and-exit, 9=Quitting
        self._game_status = 0
        self._config = {}
        self.update_config(merge_dicts(cdkkApp.default_config, app_config))
        cdkkApp._cdkkApp = self
        self._game_mgrs = {}

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

    def add_game_mgr(self, game_mgr):
        self._game_mgrs[game_mgr] = game_mgr

    def init(self):
        self._game_status = 1
        for gm in self._game_mgrs:
            gm.init_game()
        return True

    def start_game(self):
        self._game_status = 2
        for gm in self._game_mgrs:
            gm.start_game()

    def end_game(self):
        self._game_status = 3
        for gm in self._game_mgrs:
            gm.end_game()
        if self.get_config("exit_at_end"):
            self.exit_app()

    def exit_app(self):
        self._game_status = 9

    def manage_events(self):
        rkap = self.get_config("read_key_and_process")
        if rkap is not None:
            self.read_key_and_process(**rkap)

    def update(self):
        pass

    def draw(self, flip=True):
        for gm in self._game_mgrs:
            gm.draw_game()

    def manage_loop(self):
        game_over = False
        for gm in self._game_mgrs:
            game_over = game_over or gm.game_over
        if game_over:
            self.end_game()

    def cleanup(self):
        pass

    def execute(self):
        if self.init() == False:
            self._game_status = 8

        if self.get_config("auto_start"):
            self.start_game()
            self.draw()

        while self._game_status < 8:
            self.manage_events()
            self.update()
            self.draw()
            self.manage_loop()

        self.cleanup()

    def read_key_and_process(self, **kwargs):
        input_key = read_key(**kwargs)
        dealt_with = False
        for gm in self._game_mgrs:
            if not dealt_with:
                dealt_with = gm.process_input(input_key)
        return dealt_with

# --------------------------------------------------
