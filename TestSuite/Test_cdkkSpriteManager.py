import sys
sys.path.insert(0, "cdkk")
import pygame
import cdkk


# --------------------------------------------------


class Manager_TestSprite(cdkk.SpriteManager):
    def __init__(self, name="Test PyGame App Manager"):
        super().__init__(name=name)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "Plus":
                cdkk.EventManager.post_game_control("UpdateScore", score=1)
                dealt_with = True
            elif e.action == "Minus":
                cdkk.EventManager.post_game_control("UpdateScore", score=-1)
                dealt_with = True
            elif e.action == "Keyboard":
                print(e.info["key"])
        return dealt_with

# --------------------------------------------------

class Manager_Scoreboard(cdkk.SM_Scoreboard):
    def __init__(self):
        score_style = {"ypos": 200}
        timer_style = {"textcolour": "blue"}
        fps_style = {"xpos": self.app_boundary.right-150, "ypos": self.app_boundary.bottom-50,
                     "width": 150, "invisible": False}
        gameover_style = {"fillcolour": "pink"}
        super().__init__(10, score_style=score_style, timer_style=timer_style,
                         fps_style=fps_style, gameover_style=gameover_style)

# --------------------------------------------------

class TestPyGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        self.add_sprite_mgr(Manager_TestSprite(self.boundary))
        self.add_sprite_mgr(cdkk.SM_SplashScreen(self.boundary,
                                                 3, "beachball.png"))

        self.add_sprite_mgr(Manager_Scoreboard())

        key_map = {
            pygame.K_q: "Quit",
            pygame.K_s: "StartGame",
            pygame.K_c: "ClearGameOver",
            pygame.K_EQUALS: "Plus",
            pygame.K_MINUS: "Minus"
        }
        self.event_mgr.event_map(key_event_map=key_map)
        self.event_mgr.user_event(cdkk.EVENT_GAME_TIMER_1, "GameOver")
        self.event_mgr.user_event(cdkk.EVENT_GAME_TIMER_2, "ClearSplash")

# --------------------------------------------------


app_config = {
    "width": 1200, "height": 800,
    "background_fill": "burlywood",
    "caption": "Test PyGame - SpriteExtra",
    "auto_start": False,
    "image_path": "cdkk\\TestSuite\\"
}
theApp = TestPyGameApp(app_config)
theApp.execute()
