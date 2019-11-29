import sys
sys.path.insert(0, "cdkk")
import cdkk
import pygame

test_styles = {
    "Textbox1": {"textcolour": "blue", "fillcolour": None, "outlinecolour": "blue", "outlinewidth": 10},
    "Textbox2": {"textcolour": "red4", "fillcolour": "yellow2", "outlinecolour": "black"},
    "GreenFill": {"fillcolour": "green2"}
}

# --------------------------------------------------


class Manager_TestStyle(cdkk.SpriteManager):
    def __init__(self, limits, name="Test PyGame App Manager"):
        super().__init__(name)

        cdkk.stylesheet.add_stylesheet(test_styles)
        cdkk.stylesheet.add_style(cdkk.stylesheet.style("Textbox3"),
                             {"fillcolour": "white"})
        cdkk.stylesheet.add_merged_style("Textbox4",
                                    "Textbox1", "Textbox2", "GreenFill")

        textbox1 = cdkk.Sprite_TextBox("Style: Textbox1",
                                       cdkk.cdkkRect(20, 50, 300, 60), style=cdkk.stylesheet.style("Textbox1"))
        self.add(textbox1)

        textbox2 = cdkk.Sprite_TextBox("Style: Textbox2",
                                       cdkk.cdkkRect(20, 150, 300, 60), style=cdkk.stylesheet.style("Textbox2"))
        self.add(textbox2)

        textbox3 = cdkk.Sprite_TextBox("Style: Textbox3",
                                       cdkk.cdkkRect(20, 250, 300, 60), style=cdkk.stylesheet.style("Textbox3"))
        self.add(textbox3)

        textbox4 = cdkk.Sprite_TextBox("Style: Textbox4",
                                       cdkk.cdkkRect(20, 350, 300, 60), style=cdkk.stylesheet.style("Textbox4"))
        self.add(textbox4)

# --------------------------------------------------


class TestPyGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Test cdkk.Style")
        self.add_sprite_mgr(Manager_TestStyle(self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

# --------------------------------------------------


app_config = {
    "width": 1200, "height": 800,
    "background_fill": "burlywood",
    "caption": "Test PyGame - Style"
}
TestPyGameApp(app_config).execute()
