import pygame
import os 
from cdkkSprite import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

class PyGameApp:
    def __init__(self):
        self._running = True
        self._size = self._width, self._height = 1000, 700
        self._sprite_mgrs = {}
        self.display_surface = None
        self.framerate = 100
        self.background_fill = None
        self.event_mgr = EventManager()
        self._fast_keys = False
        self._key_interval = 0
        self._key_timer = None
        self._slow_update_min = 321  # msecs
        self._slow_update_timer = Timer(self._slow_update_min/1000.0)
        self._loop_timer = LoopTimer(20)

    @property
    def boundary(self):
        return (self.display_surface.get_rect())

    @property
    def loops_per_sec(self):
        return self._loop_timer.loops_per_sec

    def init(self, size=(1000,700), fullscreen=False):
        pygame.init()
        if size is not None:
            self._size = self._width, self._height = size
        if fullscreen:
            display_modes = pygame.display.list_modes()
            self._width, self._height = display_modes[0]
            self._width = self._width - 2
            self._height = self._height - 26
            self._size = (self._width, self._height)
        self.display_surface = pygame.display.set_mode(self._size)

        if not fullscreen:
            self.display_surface = pygame.display.set_mode(self._size)
        # else:
        #     self.display_surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #     self._size = self._width, self._height = self.display_surface.get_size()
        #     #self.display_surface = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._running = True

    def add_sprite_mgr(self, sprite_mgr):
        self._sprite_mgrs[sprite_mgr] = sprite_mgr

    def sprite_mgr(self, name):
        ret_sprite_mgr = None
        for sm in self._sprite_mgrs:
            if sm.name == name:
                ret_sprite_mgr = sm
        return ret_sprite_mgr

    def sprite(self, sprite_mgr_name, sprite_name):
        sm = self.sprite_mgr(sprite_mgr_name)
        return sm.sprite(sprite_name)

    def set_fast_keys(self, repeat_msecs):
        # Handle multiple keys pressed at once
        # Repeat key every repeat_msecs
        self._fast_keys = True
        self._key_interval = repeat_msecs
        self._key_timer = Timer(repeat_msecs/1000.0, EVENT_READ_KEYBOARD)

    def exit_app(self):
        self._running = False

    def event(self, e):
        dealt_with = False
        if e.type == pygame.QUIT or (e.type == EVENT_GAME_CONTROL and e.action == "Quit"):
            self.exit_app()
            dealt_with = True
            
        for sm in self._sprite_mgrs:
            if not dealt_with:
                dealt_with = sm.event(e)  # Ask each sprite manager to deal with the event

        if not dealt_with:
            dealt_with = self.event_mgr.event(e, self._fast_keys)

        return dealt_with

    def draw(self, flip=True):
        if (self.background_fill != None):
            self.display_surface.fill(colours[self.background_fill])
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
            self._running = False
 
        while( self._running ):
            for event in EventManager.get():
                self.event(event)
            self.update()
            self.draw()
            self._clock.tick(self.framerate)
            self._loop_timer.append()
            
        self.cleanup()

