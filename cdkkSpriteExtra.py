from cdkkSprite import *

### --------------------------------------------------

class Sprite_Label(Sprite_TextBox):
    default_style = {"fillcolour":None, "outlinecolour":None, "textsize":36 }

    def __init__(self, name_text="", rect=None, style=None):
        super().__init__(name_text, rect, style=merge_dicts(Sprite_Label.default_style, style), auto_size=True, name_is_text=True)
        self.draw(True)

### --------------------------------------------------

class Sprite_DynamicText(Sprite_TextBox):
    default_style = {"outlinecolour":None, "textsize":36 }

    def __init__(self, name_text="", rect=None, style=None):
        super().__init__(name_text, rect, style=merge_dicts(Sprite_DynamicText.default_style, style), auto_size=False)

### --------------------------------------------------

class Sprite_Button(Sprite_TextBox):
    default_style = {"fillcolour":"gray80", "outlinecolour":"black", "textsize":36 }

    def __init__(self, name_text, rect=None, event_on_click=None, event_on_unclick=None, style=None):
        super().__init__(name_text, rect, style=merge_dicts(Sprite_Button.default_style, style), auto_size=False, name_is_text=True)
        self.setup_mouse_events(event_on_click, event_on_unclick)

### --------------------------------------------------

class Sprite_GameOver(Sprite_TextBox):
    default_style = { "textcolour":"red3", "textsize":72, "fillcolour":"yellow1" }

    def __init__(self, rect, style=None):
        super().__init__("Game Over", rect, style=merge_dicts(Sprite_GameOver.default_style, style), auto_size=False)

### --------------------------------------------------

class Sprite_BoardGame_Board(Sprite_Shape):
    default_style = {"fillcolour":"black", "outlinecolour":None, "altcolour":"white", "highlightcolour":"violetred1", "outlinewidth":3}

    def __init__(self, name="Board", style=None):
        super().__init__(name, style=merge_dicts(Sprite_BoardGame_Board.default_style, style))
        self._rows = self._cols = 0
        self._cell0 = pygame.Rect(0,0,0,0)
        self._xsize = self._ysize = 0

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def cell_rect(self, col, row):
        x = self.rect.left + col * self._cell0.width
        y = self.rect.top + row * self._cell0.height
        return pygame.Rect(x, y, self._cell0.width, self._cell0.height)

    def setup_grid(self, xsize, cols, event_on_click=None, rows=None, ysize=None):
        self.event_on_click = event_on_click
        if ysize == None:
            ysize = xsize
        self._xsize = xsize
        self._ysize = ysize
        if rows == None:
            rows = cols
        self.rect.width = xsize * cols
        self.rect.height = ysize * rows
        self.create_canvas()

        for i in range(0,cols):
            for j in range (0,rows):
                r = cdkkRect(i * xsize, j * ysize, xsize, ysize)
                if (i+j)%2 == 0:
                    col = self.get_style_colour("fillcolour")
                else:
                    col = self.get_style_colour("altcolour")
                    if col is None:
                        col = self.get_style_colour("fillcolour")
                if col is not None:
                    pygame.draw.rect(self.image, col, r)
                img_file = self.get_style("fillimage")
                if img_file is not None:
                    img = self._load_image_from_file(img_file, scale_to=(xsize, ysize))
                    self.image.blit(img, r)
                line_col = self.get_style_colour("outlinecolour")
                line_w = self.get_style("outlinewidth")
                if line_col is not None:
                    pygame.draw.rect(self.image, line_col, r, line_w)
        self._draw_reqd = False
        self._cell0 = cdkkRect(0, 0, xsize, ysize)

    def find_cell(self, x, y, allow_outside=False):
        col = (x - self.rect.left) // self._cell0.width
        row = (y - self.rect.top) // self._cell0.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return (col, row)
        else:
            return (-1, -1)

    def highlight_cells(self, cell_list, highlight_on = True):
        for c in cell_list:
            r = cdkkRect(c[0] * self._xsize, c[1] * self._ysize, self._xsize, self._ysize)
            if highlight_on:
                col = self.get_style_colour("highlightcolour")
            else:
                col = self.get_style_colour("fillcolour")
            if col is not None:
                pygame.draw.rect(self.image, col, r)
            line_col = self.get_style_colour("outlinecolour")
            if (line_col != None):
                pygame.draw.rect(self.image, line_col, r, self.get_style("outlinewidth"))

### --------------------------------------------------

class Sprite_BoardGame_Piece(Sprite_Shape):
    default_style = { "outlinecolour":None, "shape":"Ellipse", "piecemargin":20 }

    def __init__(self, name, board, col=0, row=0, style=None):
        super().__init__(name, style=merge_dicts(Sprite_BoardGame_Piece.default_style, style))
        self._row = row
        self._col = col
        self._board = board
        self._cell = self._board.cell_rect(0,0)
        self._cell.topleft = (0,0)
        self.set_pos()
        self.create_canvas()

    def reduce_cell(self, percentage):
        r = self._cell
        r = self._cell.inflate(-int(r.width * (percentage/100.0)), -int(r.height * (percentage/100.0)))
        return r

    def set_pos(self, col=None, row=None):
        if col is not None:
            self._col = col
        if row is not None:
            self._row = row
        r = self._board.cell_rect(self._col, self._row)
        self.rect.topleft = r.topleft
        self.rect.size = r.size

    def draw(self, force_draw=False):
        if self._draw_reqd or force_draw:
            self._draw_reqd = False
            fill_col = self.get_style_colour("fillcolour")
            line_col = self.get_style_colour("outlinecolour")
            line_width = self.get_style("outlinewidth")
            margin = self.get_style("piecemargin")

            if self.get_style("shape") == "Ellipse":
                r = self.reduce_cell(margin)
                if fill_col is not None:
                    pygame.draw.ellipse(self.image, fill_col, r)
                if line_col is not None:
                    pygame.draw.ellipse(self.image, line_col, r, line_width)
            if self.get_style("shape") == "Rectangle":
                r = self.reduce_cell(margin)
                if fill_col is not None:
                    pygame.draw.rect(self.image, fill_col, r)
                if line_col is not None:
                    pygame.draw.rect(self.image, line_col, r, line_width)
            self.set_pos()

    def flip(self):
        self.swap_colours()

### --------------------------------------------------
