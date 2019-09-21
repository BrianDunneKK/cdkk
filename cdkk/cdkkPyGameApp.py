import pygame
import os 
from cdkk.cdkkSprite import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

class PyGameApp:
    default_config = {
        "caption":"CoderDojo Kilkenny",
        "width":1000,
        "height":700,
        "full_screen":False,
        "background_fill": None,
        "frame_rate":100,
        "slow_update_time":321, # msecs
        "scroll_time":None,     # msecs or None
        "key_repeat_time":None, # msecs or None
        "joystick_name":None,
        "joystick_number":None,
        "auto_start":True       # Automatically start game
        }

    def __init__(self, style=None):
        self._game_status = 0   # 0=Pre-init, 1=Initialised, 2=Game-in-progess, 3=Game over, 8=Fail-and-exit, 9=Quitting
        self._sprite_mgrs = {}
        self.display_surface = None
        self.event_mgr = EventManager()
        self._fast_keys = False
        self._key_interval = 0
        self._key_timer = None
        self._joystick = None
        self._slow_update_timer = None
        self._loop_timer = LoopTimer(20)
        self._scroll_timer = None
        self._config = {}
        self.update_config(merge_dicts(PyGameApp.default_config, style))
        self._width = self.get_config("width")
        self._height = self.get_config("height")
        self._size = (self._width, self._height)
        cdkkImage.imagePath = self.get_config("image_path")

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

    @property
    def boundary(self):
        return (self.display_surface.get_rect())

    @property
    def loops_per_sec(self):
        return self._loop_timer.loops_per_sec

    @property
    def loop_counter(self):
        return self._loop_timer.loops

    @property
    def game_in_progress(self):
        return (self._game_status == 2)

    def init(self):
        pygame.init()
        if self.get_config("full_screen"):
            display_modes = pygame.display.list_modes()
            self._width, self._height = display_modes[0]
            self._width = self._width - 2
            self._height = self._height - 26
            self._size = (self._width, self._height)
        self.display_surface = pygame.display.set_mode(self._size)

        if self.get_config("caption") is not None:
            pygame.display.set_caption(self.get_config("caption"))

        if self.get_config("key_repeat_time") is not None:
            self.set_fast_keys(self.get_config("key_repeat_time"))

        if self.get_config("scroll_time") is not None:
            self._scroll_timer = Timer(self.get_config("scroll_time")/1000.0, EVENT_SCROLL_GAME)
            self.event_mgr.user_event(EVENT_SCROLL_GAME, "ScrollGame")

        self._joystick = cdkkJoystick(self.get_config("joystick_name"), self.get_config("joystick_number"))

        self._clock = pygame.time.Clock()
        self._game_status = 1

    def add_sprite_mgr(self, sprite_mgr):
        self._sprite_mgrs[sprite_mgr] = sprite_mgr

    def sprite_mgr(self, name, **sm_config):
        ret_sprite_mgr = None
        for sm in self._sprite_mgrs:
            if sm.name == name:
                found = True
                if len(sm_config) > 0:
                    for key, value in sm_config.items():
                        found = found and (sm.get_config(key) == value)
                if found:
                    ret_sprite_mgr = sm
        return ret_sprite_mgr

    def sprite(self, sprite_mgr_name, sprite_name, **sm_config):
        sm = self.sprite_mgr(sprite_mgr_name, **sm_config)
        return sm.sprite(sprite_name)

    def set_fast_keys(self, repeat_msecs):
        # Handle multiple keys pressed at once. Repeat key every repeat_msecs
        self._fast_keys = True
        self._key_interval = repeat_msecs
        self._key_timer = Timer(repeat_msecs/1000.0, EVENT_READ_KEYBOARD)

    def config_joystick(self, limits=None, obj_size=None, steps=None):
        self._joystick.limits = limits
        if obj_size is not None:
            self._joystick.obj_size = obj_size
        if steps is not None:
            self._joystick.steps = steps
    
    def event(self, e):
        dealt_with = False
        is_broadcast = EventManager.is_broadcast(e)

        if e.type == pygame.QUIT or (e.type == EVENT_GAME_CONTROL and e.action == "Quit"):
            self.exit_app()
            dealt_with = True

        if not dealt_with and e.type == EVENT_GAME_CONTROL:
            if e.action == "StartGame":
                self.start_game()
                dealt_with = True
            elif e.action == "GameOver":
                self.end_game()
                dealt_with = True
            elif e.action == "JoystickMotion" and self._joystick is not None:
                e = self._joystick.update_event(e)

        for sm in self._sprite_mgrs:
            if (not dealt_with) or is_broadcast:
                dealt_with = sm.event(e)  # Ask each sprite manager to deal with the event

        if (not dealt_with) or is_broadcast:
            dealt_with = self.event_mgr.event(e, self._fast_keys)

        return dealt_with

    def exit_app(self):
        self._game_status = 9

    def start_game(self):
        self._game_status = 2
        for sm in self._sprite_mgrs:
            sm.start_game()

    def end_game(self):
        self._game_status = 3
        for sm in self._sprite_mgrs:
            sm.end_game()

    def draw(self, flip=True):
        if self.get_config("background_fill") is not None:
            self.display_surface.fill(colours[self.get_config("background_fill")])
        for sm in self._sprite_mgrs:
            sm.draw(self.display_surface)  # Ask each sprite manager to draw its sprites
        if flip:
            pygame.display.flip()
    
    def update(self):
        for sm in self._sprite_mgrs:
            sm.update()  # Ask each sprite manager to update its sprites
    
        if self._slow_update_timer.time_left == 0:
            for sm in self._sprite_mgrs:
                sm.slow_update()
            self._slow_update_timer.start()

    def cleanup(self):
        for sm in self._sprite_mgrs:
            sm.cleanup()
        pygame.quit()
 
    def execute(self):
        if self.init() == False:
            self._game_status = 8
 
        if self.get_config("auto_start"):
            self.start_game()

        while self._game_status < 8:
            for event in EventManager.get():
                self.event(event)
            self.update()
            self.draw()
            self._clock.tick(self.get_config("frame_rate"))
            self._loop_timer.append()
            
        self.cleanup()

