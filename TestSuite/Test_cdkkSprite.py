import sys
sys.path.append("..\cdkk")

import cdkk
import pygame

### --------------------------------------------------

class Manager_TestSprite(cdkk.SpriteManager):
    def __init__(self, limits, name = "Test PyGame App Manager"):
        super().__init__(name)

        image_sprite = cdkk.Sprite()
        image_sprite.load_image_from_file("beachball.png")
        image_sprite.rect.topleft = (10, 10)
        self.add(image_sprite)

        anim_sprite = cdkk.Sprite_Animation()
        anim_sprite.load_spritesheet("Explode", "ExplosionCount.png", 4, 4, set_anim=True)
        anim_sprite.rect.topleft = (200, 10)
        self.add(anim_sprite)

        rect_sprite = cdkk.Sprite_Shape("Shape:Rectangle", cdkk.cdkkRect(300, 10, 60, 30), {"fillcolour":"blue"})
        self.add(rect_sprite)

        ellipse_sprite = cdkk.Sprite_Shape("Shape:Ellipse", cdkk.cdkkRect(400, 10, 60, 50), {"fillcolour":"green3", "outlinecolour":"red4", "shape":"Ellipse"})
        self.add(ellipse_sprite)

        polygon_sprite = cdkk.Sprite_Shape("Shape:Polygon", cdkk.cdkkRect(500, 10, 101, 101), {"fillcolour":None, "shape":"Polygon"})
        polygon_sprite.setup_polygon([(0,50), (50,0), (100,50), (50, 100)])
        self.add(polygon_sprite)

        image_from_ss = cdkk.Sprite()
        image_from_ss._image.set_spritesheet("ExplosionCount.png", 4, 4)
        image_from_ss._image.spritesheet_image(6)
        image_from_ss._image_size_to_rect()
        image_from_ss.rect.topleft = (650, 10)
        self.add(image_from_ss)

        tb_default = cdkk.Sprite_TextBox("TextBox: Default", cdkk.cdkkRect(10, 150, 300, 60))
        self.add(tb_default)
        
        tb_style = {"textcolour":"blue", "fillcolour":None, "outlinecolour":"blue"}
        tb_style1 = cdkk.Sprite_TextBox("Blue/None/Blue", cdkk.cdkkRect(320, 150, 300, 60), style=tb_style)
        self.add(tb_style1)

        tb_style["fillcolour"] = "yellow1"
        tb_style["textsize"] = 20
        tb_style["shape"] = "Ellipse"
        tb_style2 = cdkk.Sprite_TextBox("Blue/Yellow/Blue, O, 20", cdkk.cdkkRect(640, 150, 300, 60), style=tb_style)
        self.add(tb_style2)

        tb_topleft = cdkk.Sprite_TextBox("TextBox: Top Left", cdkk.cdkkRect(10, 220, 300, 60), style={"align_horiz":"L", "align_vert":"T"})
        self.add(tb_topleft)

        tb_bottomright = cdkk.Sprite_TextBox("TextBox: Bottom Right", cdkk.cdkkRect(320, 220, 300, 60), style={"align_horiz":"R", "align_vert":"B"})
        self.add(tb_bottomright)

        tb_click_me = cdkk.Sprite_TextBox("Click Me", cdkk.cdkkRect(640, 220, 300, 60))
        ev_Clicked = cdkk.EventManager.gc_event("Clicked")
        ev_Unclicked = cdkk.EventManager.gc_event("Unclicked")
        tb_click_me.setup_mouse_events(ev_Clicked, ev_Unclicked)
        self.add(tb_click_me)

        self.game_over = cdkk.Sprite_GameOver(cdkk.cdkkRect(320, 300, 300, 60))
        ev_Clicked = cdkk.EventManager.gc_event("ToggleGameOver")
        self._click_game_over = cdkk.Sprite_Button("End Game", cdkk.cdkkRect(10, 300, 300, 60), ev_Clicked)
        self.add(self._click_game_over)
        self.start_game()

        self._fps = cdkk.Sprite_DynamicText("FPS", cdkk.cdkkRect(640, 300, 120, 40), style={"fillcolour":None, "align_horiz":"L", "textformat":"FPS: {0:4.1f}"})
        self.add(self._fps)
        self._fps_units = cdkk.Sprite_Label("frames/sec", cdkk.cdkkRect(770, 300, 150, 40))
        self._fps_units.rect.centery = 320
        self.add(self._fps_units)

        tb_auto_size = cdkk.Sprite_TextBox("AutoSize", cdkk.cdkkRect(10, 400, 0, 0), auto_size=True)
        ev_Auto_Clicked = cdkk.EventManager.gc_event("AutoSize")
        tb_auto_size.setup_mouse_events(ev_Auto_Clicked, None)
        self.add(tb_auto_size)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "Clicked":
                self.sprite("Click Me").text = "Ouch!!"
                self.sprite("Click Me").set_style("textcolour", "red1")
                dealt_with = True
            elif e.action == "Unclicked":
                self.sprite("Click Me").text = "Click Me"
                self.sprite("Click Me").set_style("textcolour", "black")
                dealt_with = True
            elif e.action == "ToggleGameOver":
                if self.game_is_active:
                    cdkk.EventManager.post_game_control("GameOver")
                else:
                    cdkk.EventManager.post_game_control("StartGame")
                dealt_with = True
            elif e.action == "AutoSize":
                t = self.sprite("AutoSize").text + "+"
                if t == "AutoSize+++++":
                    t = "AutoSize"
                self.sprite("AutoSize").text = t
                dealt_with = True
            else:
                dealt_with = False
        return dealt_with

    def start_game(self):
        super().start_game()
        self.remove(self.game_over)
        self._click_game_over.text = "End Game"

    def end_game(self):
        self.add(self.game_over)
        self._click_game_over.text = "Start Game"
        super().end_game()

    def update(self):
        self._fps.set_text(theApp.loops_per_sec)

### --------------------------------------------------

class TestPyGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Test cdkkSprite")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_TestSprite(self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

app_config = {
    "width":1200, "height":800,
    "background_fill":"burlywood",
    "caption":"Test PyGame - Sprite",
    "image_path": "TestSuite\\"
    }
theApp = TestPyGameApp(app_config)
theApp.execute()
