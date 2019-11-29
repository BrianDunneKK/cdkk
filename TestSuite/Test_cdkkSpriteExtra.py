import sys
sys.path.insert(0, "cdkk")
import pygame
import cdkk


# --------------------------------------------------


class Manager_TestSprite(cdkk.SpriteManager):
    def __init__(self, name="Test PyGame App Manager"):
        super().__init__(name)
        self._highlight = 0
        self._highlight_on = True
        cols = 8
        cell_size = 40

        self._board1 = cdkk.Sprite_BoardGame_Board(name="Board1")
        self._board1.setup_board_grid(
            cell_size, cols, cdkk.EventManager.gc_event("Board1"))
        self._board1.rect.topleft = (40, 40)
        self.add(self._board1)

        self._board2 = cdkk.Sprite_BoardGame_Board(name="Board2", style={
                                                   "fillcolour": "green", "altcolour": None, "outlinecolour": "black", "outlinewidth": 2})
        self._board2.setup_board_grid(
            cell_size, cols, cdkk.EventManager.gc_event("Board2"))
        self._board2.rect.topleft = (400, 50)
        self.add(self._board2)

        self._board3 = cdkk.Sprite_BoardGame_Board(name="Board3", style={
                                                   "fillcolour": None, "altcolour": None, "fillimage": "board.png", "outlinecolour": None})
        self._board3.setup_board_grid(cell_size, cols)
        self._board3.rect.topleft = (800, 50)
        self.add(self._board3, layer=9)

        self._piece1 = cdkk.Sprite_BoardGame_Piece(
            "Piece1", self._board3, style={"fillcolour": "red4"})
        self.add(self._piece1)
        self._piece2 = cdkk.Sprite_BoardGame_Piece("Piece2", self._board3, col=3, style={
                                                   "fillcolour": "yellow2", "piecemargin": 0})
        self.add(self._piece2)

        self._grid1 = cdkk.Sprite_ImageGrid()
        self._grid1.setup_grid((3, 2), (32, 32))
        self._grid1.setup_image_grid(
            ["ExplosionCount.png", 4, 4], [1, 3, 5, 7, 9, 11])
        self._grid1.rect.topleft = (50, 450)
        self.add(self._grid1)

        image_from_ss = cdkk.Sprite()
        image_from_ss._image.set_spritesheet("ExplosionCount.png", 4, 4)
        image_from_ss._image.spritesheet_image(6)
        image_from_ss._image_size_to_rect()
        image_from_ss.rect.topleft = (300, 450)
        self.add(image_from_ss)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "Board1":
                col, row = self._board1.find_cell(e.pos)
                print("Board 1: {0}, {1}".format(col, row))
                dealt_with = True
            elif e.action == "Board2":
                col, row = self._board2.find_cell(e.pos)
                print("Board 2: {0}, {1}".format(col, row))
                dealt_with = True
            elif e.action == "Highlight":
                self._board1.highlight_cells(
                    [(self._highlight, self._highlight)], self._highlight_on)
                self._board2.highlight_cells(
                    [(7-self._highlight, self._highlight)], self._highlight_on)
                if self._highlight == 7:
                    self._highlight_on = not self._highlight_on
                self._highlight = (self._highlight + 1) % 8
                dealt_with = True
            elif e.action == "Move":
                self._piece2.rect.move_physics(20, 20)
                dealt_with = True
        return dealt_with


# --------------------------------------------------

class TestPyGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        pygame.display.set_caption("Test cdkkSpriteExtra")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_TestSprite())
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")
        self.event_mgr.keyboard_event(pygame.K_h, "Highlight")
        self.event_mgr.keyboard_event(pygame.K_m, "Move")

# --------------------------------------------------


app_config = {
    "width": 1200, "height": 800,
    "background_fill": "burlywood",
    "caption": "Test PyGame - SpriteExtra",
    "image_path": "cdkk\\TestSuite\\"
}
theApp = TestPyGameApp(app_config)
theApp.execute()
