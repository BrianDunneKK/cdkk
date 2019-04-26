from cdkkSprite import *

### --------------------------------------------------

class Sprite_Label(Sprite_TextBox):
    default_style = {"fillcolour":None, "outlinecolour":None, "textsize":36 }

    def __init__(self, name_text="", rect=None, style=None):
        super().__init__(name_text, rect, style=merge_dicts(Sprite_Label.default_style, style), auto_size=True, name_is_text=True)

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
    default_style = { "textcolour":"red3", "textsize":72, "fillcolour":"yellow1", "outlinecolour":"red3", "outlinewidth":5, "width":400, "height":100}

    def __init__(self, rect, style=None):
        super().__init__("Game Over", rect, style=merge_dicts(Sprite_GameOver.default_style, style), auto_size=False)
        self.style_to_size()
        self.rect.center = rect.center

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

        img = None
        img_file = self.get_style("fillimage")
        if img_file is not None:
            img = cdkkImage()
            img.load(img_file, scale_to=(xsize, ysize))

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
                if img is not None:
                    self.image.blit(img.surface, r)
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

    def draw(self, draw_flag=Sprite.DRAW_AS_REQD):
        if self._draw_reqd or draw_flag:
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

class Sprite_Grid(Sprite):
    default_style = {"fillcolour":"black"}

    def __init__(self, name="Grid", style=None):
        super().__init__(name, style=merge_dicts(Sprite_Shape.invisible_style, Sprite_Grid.default_style, style))
        self._rows = self._cols = 0
        self._cell0 = pygame.Rect(0,0,0,0)
        self._xsize = self._ysize = 0

    def cell_rect(self, col, row):
        x = self.rect.left + col * self._cell0.width
        y = self.rect.top + row * self._cell0.height
        return cdkkRect(x, y, self._cell0.width, self._cell0.height)

    def setup_grid(self, spritesheet, sprites, barriers, xsize, cols, ysize=None, rows=None, event_on_click=None):
        if ysize == None:
            ysize = xsize
        self._xsize = xsize
        self._ysize = ysize

        if rows == None:
            rows = cols
        self._cols = cols
        self._rows = rows
        
        self.rect.width = xsize * cols
        self.rect.height = ysize * rows
        self._cell0 = cdkkRect(0, 0, xsize, ysize)

        self.image = self.create_surface()
        self.event_on_click = event_on_click
        self._draw_reqd = True

        self._barriers = barriers
        img = cdkkImage()
        img.set_spritesheet(spritesheet[0], spritesheet[1], spritesheet[2])
        for i in range(0,rows):
            for j in range (0,cols):
                r = cdkkRect(j * xsize, i * ysize, xsize, ysize)
                img.spritesheet_image(sprites[i*cols+j], scale_to=(xsize, ysize))
                self.image.blit(img.surface, r)

    def find_cell(self, x, y, allow_outside=False):
        col = (x - self.rect.left) // self._cell0.width
        row = (y - self.rect.top) // self._cell0.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return (col, row)
        else:
            return (-1, -1)

    def find_cellp(self, x, y, allow_outside=False):
        col, row = self.find_cell(x, y, True)
        cell = self.cell_rect(col, row)
        px = 100.0 * (x - cell.left)/cell.width
        py = 100.0 * (y - cell.top)/cell.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return [col, row, px, py]
        else:
            return [-1, -1, 0, 0]
    
    def find_barrier(self, col, row, direction):
        found = False
        bar_x = col
        bar_y = row

        if direction == "Right":
            bar_x = col + 1
            bar_y = 0
            while not found:
                found = (bar_x >= self._cols)
                if not found:
                    i = row * self._cols + bar_x
                    if i>=0 and i<len(self._barriers):
                        found = self._barriers[i]
                if not found:
                    bar_x = bar_x + 1
        elif direction == "Left":
            bar_x = col - 1
            bar_y = 0
            while not found:
                found = (bar_x < 0)
                if not found:
                    i = row * self._cols + bar_x
                    if i>=0 and i<len(self._barriers):
                        found = self._barriers[i]
                if not found:
                    bar_x = bar_x - 1
        elif direction == "Down":
            bar_y = row + 1
            bar_x = 0
            while not found:
                found = (bar_y > self._rows)
                if not found:
                    i = bar_y * self._cols + col
                    if i>=0 and i<len(self._barriers):
                        found = self._barriers[i]
                if not found:
                    bar_y = bar_y + 1
        elif direction == "Up":
            bar_y = row - 1
            bar_x = 0
            while not found:
                found = (bar_y < 0)
                if not found:
                    i = bar_y * self._cols + col
                    if i>=0 and i<len(self._barriers):
                        found = self._barriers[i]
                if not found:
                    bar_y = bar_y - 1

        if found:
            return (bar_x+bar_y)                    
        else:
            return (-1)


### --------------------------------------------------
