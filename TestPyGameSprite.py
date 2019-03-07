from PyGameApp import *

### --------------------------------------------------

class Manager_TestPGA(SpriteManager):
    def __init__(self, limits, name = "Test PyGame App Manager"):
        super().__init__(name)

        just_text = Sprite_TextBox("Test: Just Text")
        just_text.setup_text(36)
        just_text.text = "This is just text"
        just_text.rect.topleft = (50, 50)
        self.add(just_text)
        
        fmt_text = Sprite_TextBox("Test: Formatted Text")
        fmt_text.setup_text(36, "red4", ">>> {0} <-->  {1} <<<")
        fmt_text.set_text("First", "Second")
        fmt_text.rect.topleft = (500, 150)
        self.add(fmt_text)
        
        fill_text = Sprite_TextBox("Test: Fill Text")
        fill_text.setup_textbox(300, 100, "red4", 36, ["green"])
        fill_text.rect.topleft = (50, 100)
        fill_text.text = "This is filled text"
        self.add(fill_text)

        line_text = Sprite_TextBox("Test: Line Text")
        line_text.setup_textbox(500, 100, "yellow1", 36, [None, "black"])
        line_text.rect.topleft = (50, 250)
        line_text.text = "This is outlined text"
        line_text.shape = "Ellipse"
        self.add(line_text)

        linefill_text = Sprite_TextBox("Test: Line & Fill Text")
        linefill_text.setup_textbox(500, 100, "yellow1", 36, ["blue", "black"])
        linefill_text.rect.topleft = (50, 400)
        linefill_text.text = "This is filled and outlined text"
        self.add(linefill_text)

        button1 = Sprite_TextBox("Test:Button")
        button1.text = "Test-Button"
        button1.setup_textbox(200, 50, "blue", 26, ["gray80", "black"])
        button1.rect.topleft = (400, 50)
        ev_NewText = EventManager.gc_event("NewText")
        button1.setup_mouse_events(ev_NewText, None)
        self.add(button1)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == EVENT_GAME_CONTROL:
            dealt_with = True
            if e.action == "NewText":
                self.sprite("Test:Button").text = "New Text"
            else:
                dealt_with = False
        return dealt_with

### --------------------------------------------------

class TestPyGameApp(PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Test PyGame Sprite")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_TestPGA(self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

theApp = TestPyGameApp()
theApp.execute()
