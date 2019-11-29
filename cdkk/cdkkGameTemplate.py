import pygame
import cdkk

app_styles = {
    "Ninja": {"fillcolour":"yellow", "shape":"Ellipse", "width":80, "height":60}
}
cdkk.stylesheet.add_stylesheet(app_styles)

### --------------------------------------------------

class Sprite_Ninja(cdkk.Sprite_TextBox):
    def __init__(self, posx, posy):
        super().__init__("Ninja", style=cdkk.stylesheet.style("Ninja"))
        self.rect.left = posx
        self.rect.top = posy
        # Initialise the Ninja sprite

    def start_game(self):
        super().start_game()
        self.set_style("fillcolour", "green")

    def end_game(self):
        self.set_style("fillcolour", "red1")
        super().end_game()

    def update(self):
        super().update()
        # Update is called for the sprite during every game loop

    def draw(self):
        super().draw()
        # Draw is called for the sprite during every game loop


### --------------------------------------------------

class Manager_Ninja(cdkk.SpriteManager):
    def __init__(self, limits):
        super().__init__("Ninja Manager")
        self.limits = limits

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "NewNinja":
                self.add_ninja()
                dealt_with = True
            elif e.action == "ClearNinjas":
                self.clear_ninjas()
                dealt_with = True
        return dealt_with

    def move_cave_items(self):
        sprites = self.find_sprites_by_desc("Cave Item", True)
        for s in sprites:
            s.scroll(-self.cave.cave_section_size)

    def add_ninja(self):
        posx = random.randint(0, self.limits.width-200) + 100
        posy = random.randint(0, self.limits.height-150) + 75
        self.add(Sprite_Ninja(posx, posy))

    def clear_ninjas(self):
        self.empty()

    def update(self):
        super().update()
        # Update is called for the sprite during every game loop
        # For moving objects, call self.rect.move_physics()

    def start_game(self):
        super().start_game()
        # This is called each time a game starts
        # Typically this is where sprites are created/reset

    def end_game(self):
        # This is called each time a game ends
        # Typically this is where sprites are removed
        super().end_game()

### --------------------------------------------------

class Manager_Scoreboard(cdkk.SpriteManager):
    def __init__(self, game_time, limits):
        super().__init__("Scoreboard Manager")
        score_style = {"fillcolour":None, "align_horiz":"L"}

        self._game_time = game_time
        self._timer = None
        self._time_left = cdkk.Sprite_DynamicText("Time Left", cdkk.cdkkRect(10, 10, 200, 40), score_style)
        self._time_left.set_text_format("Time Left: {0:0.1f}", 0)
        self.add(self._time_left)

        self._fps = cdkk.Sprite_DynamicText("FPS", cdkk.cdkkRect(10, 60, 200, 40), score_style)
        self._fps.set_text_format("FPS: {0:4.1f}", 0)
        self.add(self._fps)

        self._game_over = cdkk.Sprite_GameOver(limits)

    def set_fps(self, new_fps):
        self._fps.set_text(new_fps)

    def slow_update(self):
        # This is called around 3 times per sec and is for updates that don't need to happen every game loop
        if self.game_is_active:
            self._time_left.set_text(self._timer.time_left)
            
    def start_game(self):
        super().start_game()
        self._timer = cdkk.Timer(self._game_time, cdkk.EVENT_GAME_TIMER_1, auto_start=True)
        self.remove(self._game_over)

    def end_game(self):
        self.add(self._game_over)
        super().end_game()

### --------------------------------------------------

class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()

        self.ninja_mgr = Manager_Ninja(self.boundary)
        self.scoreboard_mgr = Manager_Scoreboard(10, self.boundary)

        self.add_sprite_mgr(self.ninja_mgr)
        self.add_sprite_mgr(self.scoreboard_mgr)

        key_map = {
            pygame.K_q : "Quit",
            pygame.K_s : "StartGame",
            pygame.K_n : "NewNinja",
            pygame.K_c : "ClearNinjas"
        }
        user_event_map = {
            cdkk.EVENT_GAME_TIMER_1 : "GameOver"
        }
        self.event_mgr.event_map(key_event_map=key_map, user_event_map=user_event_map)

    def update(self):
        super().update()
        self.scoreboard_mgr.set_fps(theApp.loops_per_sec)
        # Manage interaction between Sprites in different SpriteManagers

### --------------------------------------------------

app_config = {
    "width":1200, "height":800,
    "background_fill":"burlywood",
    "caption":"My Game",
    "auto_start":False
    }
theApp = MyGame(app_config)
theApp.execute()
