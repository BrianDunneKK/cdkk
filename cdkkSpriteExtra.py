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

class Sprite_Grid(Sprite):
    default_style = Sprite_Shape.invisible_style

    def __init__(self, name="Grid", style=None):
        super().__init__(name, style=merge_dicts(Sprite_Grid.default_style, style))
        self._rows = self._cols = 0
        self._cell0 = pygame.Rect(0,0,0,0)
        self._xsize = self._ysize = 0

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def cell_size(self):
        return (self._xsize, self._ysize)

    def setup_grid(self, cols_rows, xsize_ysize, event_on_click=None):
        xsize, ysize = xsize_ysize
        if ysize is None: ysize = xsize
        self._xsize = xsize
        self._ysize = ysize

        cols, rows = cols_rows
        if rows is None: rows = cols
        self._cols = cols
        self._rows = rows

        self.rect.width = xsize * cols
        self.rect.height = ysize * rows
        self._cell0 = cdkkRect(0, 0, xsize, ysize)

        self.image = self.create_surface()
        self.event_on_click = event_on_click
    
    def cell_rect(self, col, row, relative=False):
        x = col * self._cell0.width
        y = row * self._cell0.height
        if not relative:
            x = x + self.rect.left
            y = y + self.rect.top
        return cdkkRect(x, y, self._cell0.width, self._cell0.height)

    def find_cell(self, x_y, allow_outside=False):
        x, y = x_y
        col = (x - self.rect.left) // self._cell0.width
        row = (y - self.rect.top) // self._cell0.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return (col, row)
        else:
            return (-1, -1)

    def find_cellp(self, x_y, allow_outside=False):
        x, y = x_y
        col, row = self.find_cell(x_y, True)
        cell = self.cell_rect(col, row)
        px = 100.0 * (x - cell.left)/cell.width
        py = 100.0 * (y - cell.top)/cell.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return [col, row, px, py]
        else:
            return [-1, -1, 0, 0]

    def find_cell_centre(self, x_y, allow_outside=False):
        cellp = self.find_cellp(x_y, allow_outside)
        px = cellp[2]
        py = cellp[3]

        if (px>35 and px<65 and py>35 and py<65):
            return (cellp[0], cellp[1])
        else:
            return (-1, -1)

### --------------------------------------------------

class Sprite_BoardGame_Board(Sprite_Grid):
    default_style = {"fillcolour":"black", "outlinecolour":None, "altcolour":"white", "highlightcolour":"violetred1", "outlinewidth":3}

    def __init__(self, name="Board", style=None):
        super().__init__(name, style=merge_dicts(Sprite_BoardGame_Board.default_style, style))

    def setup_board_grid(self, xsize, cols, event_on_click=None, rows=None, ysize=None):
        super().setup_grid((cols, rows), (xsize, ysize), event_on_click)

        img = None
        img_file = self.get_style("fillimage")
        if img_file is not None:
            img = cdkkImage()
            img.load(img_file, scale_to=self.cell_size)

        for i in range(0,self.cols):
            for j in range (0,self.rows):
                r = self.cell_rect(i,j, True)
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

    def highlight_cells(self, cell_list, highlight_on = True):
        for c in cell_list:
            r = self.cell_rect(c[0], c[1], True)
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

class Sprite_ImageGrid(Sprite_Grid):
    default_style = {"fillcolour":"black"}

    def __init__(self, name="Grid", style=None):
        super().__init__(name, style=merge_dicts(Sprite_Shape.invisible_style, Sprite_ImageGrid.default_style, style))

    def setup_image_grid(self, spritesheet, sprites, barriers, xsize, cols, ysize=None, rows=None, event_on_click=None):
        super().setup_grid((cols, rows), (xsize, ysize), event_on_click)

        self._barriers = barriers
        img = cdkkImage()
        img.set_spritesheet(spritesheet[0], spritesheet[1], spritesheet[2])
        for i in range(0,rows):
            for j in range (0,cols):
                r = cdkkRect(j * xsize, i * ysize, xsize, ysize)
                img.spritesheet_image(sprites[i*cols+j], scale_to=(xsize, ysize))
                self.image.blit(img.surface, r)

### --------------------------------------------------

class Sprite_ImageGridActor(Sprite_Animation):
    def __init__(self, name, start_cell, cell0, speed=1, move_timer=None):
        super().__init__(name)
        self._cell_pos = [None, None, None, None]  # cell_x, cell_y, cell_px, cell_py
        self._barriers = None
        self.direction = "R"
        self._speed = speed
        self._cell0 = cell0
        self.load_image()
        self.move_to(start_cell)
        self._timer = Timer(move_timer) if move_timer is not None else None

    @property
    def centre(self):
        return self.rect.center

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if new_direction in ["U", "D", "L", "R"]:
            self._direction = new_direction
            self.set_animation(self.name + new_direction, ANIMATE_SHUTTLE, 2)
            self._draw_reqd = True

    def set_pos(self, new_cell_pos, new_barriers=None):
        self._cell_pos = new_cell_pos
        self._barriers = new_barriers

    def _convert_dir(self, dir):
        # Convert dir string to dx, dy
        if   dir == "R": dx, dy = 1, 0
        elif dir == "L": dx, dy = -1, 0
        elif dir == "D": dx, dy = 0, 1
        elif dir == "U": dx, dy = 0, -1
        else: dx, dy = 0, 0
        return (dx, dy)

    def _can_move(self):
        x = self._cell_pos[0]
        y = self._cell_pos[1]
        px = self._cell_pos[2]
        py = self._cell_pos[3]

        dir_ok = { "R":True, "L":True, "D":True, "U":True }

        # Check if barrier is too close
        if px >= 50: dir_ok["R"] = ((x+1) < self._barriers["R"]) and (py>35 and py<65)
        if px <= 50: dir_ok["L"] = ((x-1) > self._barriers["L"]) and (py>35 and py<65)
        if py >= 50: dir_ok["D"] = ((y+1) < self._barriers["D"]) and (px>35 and px<65)
        if py <= 50: dir_ok["U"] = ((y-1) > self._barriers["U"]) and (px>35 and px<65)

        return dir_ok

    def move(self, dir=None):
        if dir is None:
            dir = self.choose_move(self._can_move())

        if dir not in ["R", "L", "D", "U"]:
            return

        dir_ok = self._can_move()

        dx = dy = 0
        if dir == "R" and dir_ok["R"]: dx = self._speed
        if dir == "L" and dir_ok["L"]: dx = -self._speed
        if dir == "D" and dir_ok["D"]: dy = self._speed
        if dir == "U" and dir_ok["U"]: dy = -self._speed

        if dir_ok[dir]:
            if dx != 0: dy = ((50 - self._cell_pos[3]) / 100.0 ) * self._cell0.height
            if dy != 0: dx = ((50 - self._cell_pos[2]) / 100.0 ) * self._cell0.width
            self.direction = dir
            self.move_by(dx, dy)

        return dir_ok[dir]

    def move_by(self, dx, dy):
        do_move = True
        if self._timer is not None:
            do_move = self._timer.time_up()

        if do_move: self.rect.move_physics(dx, dy)

    def move_to(self, col_row, new_dir=None):
        col, row = col_row
        self.rect.centerx = self._cell0.left + (col + 0.5) * self._cell0.width
        self.rect.centery = self._cell0.top + (row + 0.5) * self._cell0.height
        self._cell_pos = [col, row, 50, 50]
        if new_dir is not None:
            self.direction = new_dir

    def choose_move(self, can_move):
        return "R"

### --------------------------------------------------
